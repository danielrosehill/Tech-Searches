#!/usr/bin/env python3
"""
Tech Searches Formatting Agent

This agent processes notes from the preformatted directory and formats them
according to the system prompt using Ollama's qwen2.5:14b model.
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path
import requests
from datetime import datetime

class FormattingAgent:
    def __init__(self, model_name="qwen2.5:14b-instruct-q5_K_M"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"
        self.repo_root = Path(__file__).parent.parent.parent
        self.preformatted_dir = self.repo_root / "preformatted"
        self.processed_dir = self.repo_root / "processed"
        self.system_prompt_file = self.repo_root / "processing" / "formatting-agent" / "system-prompt.md"
        
        # Ensure processed directory exists
        self.processed_dir.mkdir(exist_ok=True)
        
    def load_system_prompt(self):
        """Load the system prompt from the markdown file."""
        try:
            with open(self.system_prompt_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Error: System prompt file not found at {self.system_prompt_file}")
            sys.exit(1)
    
    def get_preformatted_files(self):
        """Get list of markdown files in preformatted directory and subdirectories."""
        if not self.preformatted_dir.exists():
            print(f"Error: Preformatted directory not found at {self.preformatted_dir}")
            return []
        
        return list(self.preformatted_dir.glob("**/*.md"))
    
    def format_with_ollama(self, content, system_prompt):
        """Send content to Ollama for formatting."""
        prompt = f"""System: {system_prompt}

User: Please format the following text according to the system instructions:

{content}"""
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9
            }
        }
        
        try:
            print(f"Sending request to Ollama with model {self.model_name}...")
            response = requests.post(self.ollama_url, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '').strip()
            
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing Ollama response: {e}")
            return None
    
    def process_file(self, file_path):
        """Process a single markdown file."""
        print(f"Processing: {file_path.name}")
        
        # Read the original content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return False
        
        # Load system prompt
        system_prompt = self.load_system_prompt()
        
        # Format with Ollama
        formatted_content = self.format_with_ollama(content, system_prompt)
        
        if formatted_content is None:
            print(f"Failed to format {file_path.name}")
            return False
        
        # Create output filename with human-readable timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        base_name = file_path.stem  # filename without extension
        output_file = self.repo_root / f"{base_name}-{timestamp}.md"
        
        # Add metadata header with human-readable timestamp
        readable_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        final_content = f"""<!-- Formatted by Tech Searches Formatting Agent -->
<!-- Original file: {file_path.name} -->
<!-- Processed: {readable_timestamp} -->
<!-- Model: {self.model_name} -->

{formatted_content}"""
        
        # Write formatted content
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_content)
            print(f"✓ Formatted content saved to: {output_file.name}")
            
            # Move original file to processed directory
            processed_file = self.processed_dir / file_path.name
            shutil.move(str(file_path), str(processed_file))
            print(f"✓ Original file moved to: processed/{file_path.name}")
            
            return True
        except Exception as e:
            print(f"Error writing {output_file} or moving original: {e}")
            return False
    
    def process_all_files(self):
        """Process all markdown files in preformatted directory."""
        files = self.get_preformatted_files()
        
        if not files:
            print("No markdown files found in preformatted directory.")
            return
        
        print(f"Found {len(files)} file(s) to process.")
        
        successful = 0
        for file_path in files:
            if self.process_file(file_path):
                successful += 1
        
        print(f"\nProcessing complete: {successful}/{len(files)} files formatted successfully.")
    
    def process_single_file(self, file_input):
        """Process a specific file by path or name."""
        # Handle different input formats
        if file_input.startswith('preformatted/'):
            # Full path from repo root
            file_path = self.repo_root / file_input
        elif '/' in file_input:
            # Relative path within preformatted
            file_path = self.preformatted_dir / file_input
        else:
            # Just filename - search in preformatted and subdirs
            matches = list(self.preformatted_dir.glob(f"**/{file_input}"))
            if not matches:
                print(f"Error: File '{file_input}' not found in preformatted directory or subdirectories.")
                return False
            elif len(matches) > 1:
                print(f"Error: Multiple files named '{file_input}' found:")
                for match in matches:
                    rel_path = match.relative_to(self.preformatted_dir)
                    print(f"  - {rel_path}")
                print("Please specify the full path.")
                return False
            file_path = matches[0]
        
        if not file_path.exists():
            print(f"Error: File '{file_input}' not found.")
            return False
        
        return self.process_file(file_path)


def main():
    parser = argparse.ArgumentParser(description='Format tech search notes using Ollama')
    parser.add_argument('--file', '-f', help='Process specific file (supports full paths, relative paths, or just filename)')
    parser.add_argument('--model', '-m', default='qwen2.5:14b-instruct-q5_K_M', 
                       help='Ollama model to use (default: qwen2.5:14b-instruct-q5_K_M)')
    parser.add_argument('--list-files', '-l', action='store_true', 
                       help='List available files in preformatted directory')
    
    args = parser.parse_args()
    
    agent = FormattingAgent(model_name=args.model)
    
    if args.list_files:
        files = agent.get_preformatted_files()
        if files:
            print("Available files in preformatted directory:")
            for file_path in files:
                print(f"  - {file_path.name}")
        else:
            print("No markdown files found in preformatted directory.")
        return
    
    if args.file:
        agent.process_single_file(args.file)
    else:
        agent.process_all_files()


if __name__ == "__main__":
    main()
