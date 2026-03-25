#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown to Word Converter (Standard Official Format)
Convert Markdown files to Word documents with official document formatting.
"""

import argparse
import subprocess
import sys
import os
import re
from pathlib import Path
import shutil
from datetime import datetime


class MD2DocxConverter:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.template_dir = self.script_dir
        self.default_template = self.template_dir / "songti-template.docx"
        
    def convert(self, input_file, output_dir=None, no_toc=False, custom_template=None, no_template=False):
        """
        Convert markdown file to docx with official formatting
        
        Args:
            input_file: Input markdown file path
            output_dir: Output directory (optional, defaults to input file dir)
            no_toc: Whether to exclude table of contents
            custom_template: Custom template file (optional)
            no_template: Don't use template, keep default formatting
        """
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
            
        # Determine output directory
        if output_dir:
            output_path = Path(output_dir)
        else:
            output_path = input_path.parent
            
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate output filename
        output_filename = f"{input_path.stem}.docx"
        output_file = output_path / output_filename
        
        # 为了将日期放在文档末尾，我们先临时修改 Markdown 文件内容
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 在文档末尾添加日期
        date_line = f"\n\n---\n\n{datetime.now().strftime('%Y年%m月%d日')}"
        
        # 修复表格格式：在粗体文本后的表格前加空行
        # pandoc 需要表格前有空行才能正确识别
        content = re.sub(r'(\*\*\d+\.\s+[^\*]+\*\*)\n(\|)', r'\1\n\n\2', content)
        
        temp_input_path = input_path.with_suffix('.temp.md')
        with open(temp_input_path, 'w', encoding='utf-8') as f:
            f.write(content + date_line)
        
        # Prepare pandoc arguments
        cmd = [
            "pandoc",
            str(temp_input_path),
        ]
        
        # Add table of contents if not disabled
        if not no_toc:
            cmd.extend(["--toc", "--toc-depth=3"])
        
        # Add template if not disabled
        if not no_template:
            cmd.append("--reference-doc=" + str(custom_template or self.default_template))
        
        # Output file
        cmd.extend(["-o", str(output_file)])
        
        # Additional options for better formatting
        cmd.extend([
            "--pdf-engine=wkhtmltopdf",  # Not used for docx but for consistency
            "--standalone",              # Standalone document
            "--columns", "80"            # Text width
        ])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            # 清理临时文件
            if temp_input_path.exists():
                temp_input_path.unlink()
            print(f"OK Successfully converted: {input_path.name} -> {output_file.name}")
            return str(output_file)
        except subprocess.CalledProcessError as e:
            # 清理临时文件
            if temp_input_path.exists():
                temp_input_path.unlink()
            print(f"ERROR Error converting {input_path.name}: {e.stderr}")
            raise
        except FileNotFoundError:
            # 清理临时文件
            if temp_input_path.exists():
                temp_input_path.unlink()
            print("ERROR Pandoc not found. Please install pandoc: https://pandoc.org/installing.html")
            raise


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to Word with official document formatting")
    parser.add_argument("input_files", nargs="+", help="Input markdown files to convert")
    parser.add_argument("-o", "--output", help="Output directory (default: same as input)")
    parser.add_argument("--no-toc", action="store_true", help="Don't generate table of contents")
    parser.add_argument("-t", "--template", help="Custom template file")
    parser.add_argument("--no-template", action="store_true", help="Don't use template, keep default formatting")
    parser.add_argument("--no-font", action="store_true", help="Don't apply font settings")
    
    args = parser.parse_args()
    
    converter = MD2DocxConverter()
    
    # Check if template exists
    if not converter.default_template.exists():
        print(f"WARNING Warning: Default template not found: {converter.default_template}")
        print("Please ensure 'standard-official-template.docx' exists in the tools directory.")
    
    success_count = 0
    for input_file in args.input_files:
        try:
            output_file = converter.convert(
                input_file,
                output_dir=args.output,
                no_toc=args.no_toc,
                custom_template=args.template,
                no_template=args.no_template
            )
            success_count += 1
        except Exception as e:
            print(f"Failed to convert {input_file}: {str(e)}")
    
    print(f"\nOK Conversion completed: {success_count}/{len(args.input_files)} files successful")


if __name__ == "__main__":
    main()