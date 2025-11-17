#!/usr/bin/env python3
"""
WOZ Controller for Misty Marketing Scripts
Allows human operator to select and run different marketing technique scripts
"""

import os
import importlib.util
import sys
from pathlib import Path

class WOZController:
    def __init__(self):
        self.scripts_dir = Path(__file__).parent / "scripts"
        self.scripts = self.load_scripts()
        
    def load_scripts(self):
        """Load all available script files"""
        scripts = {}
        if not self.scripts_dir.exists():
            print("Scripts directory not found!")
            return scripts
            
        for script_file in self.scripts_dir.glob("*.py"):
            if script_file.name != "__init__.py":
                script_name = script_file.stem.replace("_", " ").title()
                scripts[script_name] = script_file
                
        return scripts
    
    def display_menu(self):
        """Display available scripts menu"""
        print("\n" + "="*50)
        print("    WOZ CONTROLLER - MISTY MARKETING SCRIPTS")
        print("="*50)
        print("Available Scripts:")
        print("-" * 20)
        
        for i, (name, _) in enumerate(self.scripts.items(), 1):
            print(f"{i}. {name}")
            
        print(f"{len(self.scripts) + 1}. Exit")
        print("-" * 20)
        
    def show_script_preview(self, script_path):
        """Show preview of script content"""
        try:
            with open(script_path, 'r') as f:
                content = f.read()
                print(f"\n--- Preview of {script_path.name} ---")
                print(content[:200] + "..." if len(content) > 200 else content)
                print("-" * 40)
        except Exception as e:
            print(f"Error reading script: {e}")
    
    def run_script(self, script_path):
        """Execute the selected script"""
        try:
            # Load and execute the script
            spec = importlib.util.spec_from_file_location("script_module", script_path)
            script_module = importlib.util.module_from_spec(spec)
            
            print(f"\n🤖 Running: {script_path.name}")
            print("="*40)
            
            # Execute the script module
            spec.loader.exec_module(script_module)
            
            # Call the run_script function if it exists
            if hasattr(script_module, 'run_script'):
                script_module.run_script()
            else:
                print("⚠️ No run_script() function found in script")
            
            print("="*40)
            print("✅ Script completed!")
            
        except Exception as e:
            print(f"❌ Error running script: {e}")
            import traceback
            traceback.print_exc()
    
    def run(self):
        """Main control loop"""
        while True:
            self.display_menu()
            
            try:
                choice = input("\nSelect script to run (number): ").strip()
                
                if not choice.isdigit():
                    print("❌ Please enter a valid number!")
                    continue
                    
                choice = int(choice)
                
                if choice == len(self.scripts) + 1:
                    print("👋 Goodbye!")
                    break
                    
                if 1 <= choice <= len(self.scripts):
                    script_name = list(self.scripts.keys())[choice - 1]
                    script_path = self.scripts[script_name]
                    
                    # Show preview
                    self.show_script_preview(script_path)
                    
                    # Confirm execution
                    confirm = input(f"\nRun '{script_name}'? (y/n): ").strip().lower()
                    if confirm in ['y', 'yes']:
                        self.run_script(script_path)
                    else:
                        print("❌ Script cancelled")
                else:
                    print("❌ Invalid choice! Please select a valid number.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Pause before showing menu again
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    controller = WOZController()
    controller.run()