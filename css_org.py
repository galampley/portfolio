from cssutils import CSSParser

def organize_css_with_cssutils(css_content):
    organized_css_str = ''
    css_sheet = None  # Initialize to None

    # Try to read and parse the CSS file
    try:
        with open('styles.css', 'r') as f:
            css_content = f.read()
            print(f"CSS Content: {css_content[:100]}...")  # Print first 100 characters

        parser = CSSParser()
        css_sheet = parser.parseString(css_content)
        print("Successfully parsed the CSS content.")
    except Exception as e:
        print(f"An error occurred while parsing: {e}")
        return None  # Return None if an exception occurs

    # Proceed only if css_sheet is successfully parsed
    if css_sheet:
        for rule in css_sheet:
            if rule.type == rule.STYLE_RULE:
                organized_css_str += f"{rule.selectorText} {{\n"
                for property in rule.style:
                    organized_css_str += f"    {property.name}: {property.value};\n"
                organized_css_str += '}\n\n'
            elif rule.type == rule.MEDIA_RULE:
                organized_css_str += f"@media {rule.media.mediaText} {{\n"
                for sub_rule in rule:
                    if sub_rule.type == sub_rule.STYLE_RULE:
                        organized_css_str += f"    {sub_rule.selectorText} {{\n"
                        for property in sub_rule.style:
                            organized_css_str += f"        {property.name}: {property.value};\n"
                        organized_css_str += '    }\n'
                organized_css_str += '}\n\n'

    return organized_css_str

# Try to use the function and save the organized CSS
try:
    organized_css_content_enhanced = organize_css_with_cssutils(None)  # Passing None for now
    if organized_css_content_enhanced is not None:
        with open('organized_styles_enhanced.css', 'w') as f:
            f.write(organized_css_content_enhanced)
        print("CSS successfully organized and saved.")
    else:
        print("Failed to organize CSS.")
except Exception as e:
    print(f"An outer exception occurred: {e}")

