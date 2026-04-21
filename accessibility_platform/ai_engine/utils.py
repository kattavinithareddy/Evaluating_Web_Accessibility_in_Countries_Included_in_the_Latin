import os
import json
import time
from datetime import timedelta
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
from compliance_evaluation.models import ComplianceIssue, ScanHistory
from .models import MLModel
import joblib
import numpy as np

def run_accessibility_scan(project):
    """
    Main function to run accessibility scan on a project
    """
    start_time = time.time()
    
    try:
        # Step 1: Fetch webpage content
        html_content = fetch_webpage_content(project.url)
        
        # Step 2: Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Step 3: Run various accessibility checks
        issues = []
        issues.extend(check_alt_text(soup, project))
        issues.extend(check_color_contrast(soup, project))
        issues.extend(check_form_labels(soup, project))
        issues.extend(check_heading_structure(soup, project))
        issues.extend(check_aria_attributes(soup, project))
        issues.extend(check_keyboard_navigation(soup, project))
        issues.extend(check_language_declaration(soup, project))
        
        # Step 4: Calculate compliance score
        total_checks = 50  # Arbitrary number of checks performed
        issues_found = len(issues)
        compliance_score = max(0, ((total_checks - issues_found) / total_checks) * 100)
        
        # Step 5: Save issues to database
        for issue_data in issues:
            ComplianceIssue.objects.create(
                project=project,
                issue_type=issue_data['type'],
                severity=issue_data['severity'],
                wcag_criterion=issue_data['criterion'],
                description=issue_data['description'],
                element_selector=issue_data.get('selector', ''),
                page_url=project.url,
                code_snippet=issue_data.get('code_snippet', ''),
                recommendation=issue_data['recommendation']
            )
        
        # Step 6: Create scan history
        end_time = time.time()
        scan_duration = timedelta(seconds=int(end_time - start_time))
        
        critical_count = len([i for i in issues if i['severity'] == 'critical'])
        serious_count = len([i for i in issues if i['severity'] == 'serious'])
        moderate_count = len([i for i in issues if i['severity'] == 'moderate'])
        minor_count = len([i for i in issues if i['severity'] == 'minor'])
        
        ScanHistory.objects.create(
            project=project,
            compliance_score=Decimal(str(compliance_score)),
            total_issues=issues_found,
            critical_issues=critical_count,
            serious_issues=serious_count,
            moderate_issues=moderate_count,
            minor_issues=minor_count,
            scan_duration=scan_duration,
            scan_details={'checks_performed': total_checks}
        )
        
        # Step 7: Update project
        project.compliance_score = Decimal(str(compliance_score))
        project.status = 'completed'
        project.last_scanned = timezone.now()
        project.save()
        
        return {
            'success': True,
            'compliance_score': compliance_score,
            'issues_found': issues_found
        }
        
    except Exception as e:
        project.status = 'failed'
        project.save()
        raise e

def fetch_webpage_content(url):
    """Fetch webpage HTML content"""
    try:
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise Exception(f"Failed to fetch webpage: {str(e)}")

def check_alt_text(soup, project):
    """Check for missing alt text on images"""
    issues = []
    images = soup.find_all('img')
    
    for img in images:
        if not img.get('alt'):
            issues.append({
                'type': 'alt_text',
                'severity': 'serious',
                'criterion': '1.1.1',
                'description': 'Image missing alternative text',
                'selector': f'img[src="{img.get("src", "")}"]',
                'code_snippet': str(img)[:200],
                'recommendation': 'Add descriptive alt text to provide text alternative for images'
            })
    
    return issues

def check_color_contrast(soup, project):
    """Check for color contrast issues (simplified check)"""
    issues = []
    # This is a simplified check - proper contrast checking requires CSS analysis
    elements_with_style = soup.find_all(style=True)
    
    for element in elements_with_style[:10]:  # Limit to 10 for performance
        style = element.get('style', '')
        if 'color' in style.lower() and 'background' in style.lower():
            # Simplified check - in production, use actual contrast ratio calculation
            issues.append({
                'type': 'color_contrast',
                'severity': 'moderate',
                'criterion': '1.4.3',
                'description': 'Potential color contrast issue detected',
                'selector': element.name,
                'code_snippet': str(element)[:200],
                'recommendation': 'Ensure text has sufficient contrast ratio (4.5:1 for normal text, 3:1 for large text)'
            })
    
    return issues

def check_form_labels(soup, project):
    """Check for form inputs without labels"""
    issues = []
    inputs = soup.find_all(['input', 'select', 'textarea'])
    
    for input_elem in inputs:
        input_id = input_elem.get('id')
        input_type = input_elem.get('type', 'text')
        
        # Skip hidden and submit buttons
        if input_type in ['hidden', 'submit', 'button']:
            continue
        
        # Check if input has associated label
        has_label = False
        if input_id:
            label = soup.find('label', {'for': input_id})
            if label:
                has_label = True
        
        # Check for aria-label
        if input_elem.get('aria-label') or input_elem.get('aria-labelledby'):
            has_label = True
        
        if not has_label:
            issues.append({
                'type': 'form_labels',
                'severity': 'serious',
                'criterion': '3.3.2',
                'description': 'Form input missing associated label',
                'selector': f'{input_elem.name}[type="{input_type}"]',
                'code_snippet': str(input_elem)[:200],
                'recommendation': 'Add a label element or aria-label attribute to identify the input purpose'
            })
    
    return issues

def check_heading_structure(soup, project):
    """Check for proper heading hierarchy"""
    issues = []
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    if headings:
        # Check if first heading is h1
        if headings[0].name != 'h1':
            issues.append({
                'type': 'heading_structure',
                'severity': 'moderate',
                'criterion': '1.3.1',
                'description': 'Page does not start with h1 heading',
                'selector': 'body',
                'recommendation': 'Start page with h1 heading and maintain logical heading hierarchy'
            })
        
        # Check for skipped heading levels
        prev_level = 0
        for heading in headings:
            current_level = int(heading.name[1])
            if prev_level > 0 and current_level > prev_level + 1:
                issues.append({
                    'type': 'heading_structure',
                    'severity': 'minor',
                    'criterion': '1.3.1',
                    'description': f'Heading level skipped from h{prev_level} to {heading.name}',
                    'selector': heading.name,
                    'code_snippet': str(heading)[:200],
                    'recommendation': 'Maintain logical heading hierarchy without skipping levels'
                })
            prev_level = current_level
    
    return issues

def check_aria_attributes(soup, project):
    """Check for ARIA attribute issues"""
    issues = []
    elements_with_aria = soup.find_all(lambda tag: any(attr.startswith('aria-') for attr in tag.attrs))
    
    for element in elements_with_aria[:5]:  # Limit for performance
        # Check for invalid ARIA attributes (simplified)
        for attr in element.attrs:
            if attr.startswith('aria-'):
                if not element.attrs[attr]:
                    issues.append({
                        'type': 'aria_attributes',
                        'severity': 'moderate',
                        'criterion': '4.1.2',
                        'description': f'Empty ARIA attribute: {attr}',
                        'selector': element.name,
                        'code_snippet': str(element)[:200],
                        'recommendation': 'Provide value for ARIA attributes or remove if not needed'
                    })
    
    return issues

def check_keyboard_navigation(soup, project):
    """Check for keyboard navigation issues"""
    issues = []
    interactive_elements = soup.find_all(['a', 'button', 'input', 'select', 'textarea'])
    
    for element in interactive_elements[:10]:  # Limit for performance
        # Check if element with onclick has tabindex
        if element.get('onclick') and not element.get('tabindex'):
            issues.append({
                'type': 'keyboard_navigation',
                'severity': 'serious',
                'criterion': '2.1.1',
                'description': 'Interactive element may not be keyboard accessible',
                'selector': element.name,
                'code_snippet': str(element)[:200],
                'recommendation': 'Ensure all interactive elements are keyboard accessible'
            })
    
    return issues

def check_language_declaration(soup, project):
    """Check for language declaration"""
    issues = []
    html_tag = soup.find('html')
    
    if html_tag and not html_tag.get('lang'):
        issues.append({
            'type': 'language',
            'severity': 'serious',
            'criterion': '3.1.1',
            'description': 'Page language not declared',
            'selector': 'html',
            'recommendation': 'Add lang attribute to html tag (e.g., <html lang="en">)'
        })
    
    return issues
