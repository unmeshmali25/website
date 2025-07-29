import os
import re

def fix_date_format_in_posts(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            
            with open(filepath, 'r') as f:
                content = f.read()

            # Correct the date format to be a proper TOML string
            # The key is to wrap the date in quotes
            new_content = re.sub(
                r'(date = )([\d-T:]+)',
                r'\1"\2"',
                content
            )

            if new_content != content:
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"Corrected date format in {filename}")

if __name__ == "__main__":
    weekly_posts_dir = os.path.join("content", "posts", "weekly")
    if os.path.isdir(weekly_posts_dir):
        fix_date_format_in_posts(weekly_posts_dir)
    else:
        print(f"Directory not found: {weekly_posts_dir}") 