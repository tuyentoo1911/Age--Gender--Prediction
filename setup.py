#!/usr/bin/env python3
"""
Quick setup script for Face Prediction Django Application
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def setup_virtual_environment():
    """Create and activate virtual environment"""
    if not os.path.exists('venv'):
        run_command('python -m venv venv', 'Creating virtual environment')
    
    # Activation command varies by OS
    if os.name == 'nt':  # Windows
        activate_cmd = 'venv\\Scripts\\activate.bat'
        pip_cmd = 'venv\\Scripts\\pip'
    else:  # Unix/Linux/macOS
        activate_cmd = 'source venv/bin/activate'
        pip_cmd = 'venv/bin/pip'
    
    print(f"💡 To activate virtual environment, run: {activate_cmd}")
    return pip_cmd

def install_dependencies(pip_cmd):
    """Install required Python packages"""
    requirements_file = 'django_requirements.txt'
    if os.path.exists(requirements_file):
        run_command(f'{pip_cmd} install -r {requirements_file}', 'Installing dependencies')
    else:
        print(f"❌ {requirements_file} not found")
        return False
    return True

def setup_database():
    """Set up Django database"""
    run_command('python manage.py migrate', 'Setting up database')
    
    # Create superuser automatically (for demo purposes)
    create_superuser_script = '''
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin123")
    print("✅ Superuser created: admin/admin123")
else:
    print("ℹ️ Superuser already exists")
'''
    
    with open('create_superuser.py', 'w') as f:
        f.write(create_superuser_script)
    
    run_command('python manage.py shell < create_superuser.py', 'Creating superuser')
    os.remove('create_superuser.py')

def collect_static_files():
    """Collect static files"""
    run_command('python manage.py collectstatic --noinput', 'Collecting static files')

def copy_model_files():
    """Copy ML model files to the correct location"""
    models_dir = 'models'
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"📁 Created {models_dir} directory")
    
    model_files = ['best_gender_model.h5', 'best_age_model.h5']
    for model_file in model_files:
        if os.path.exists(model_file):
            dest_path = os.path.join(models_dir, model_file)
            if not os.path.exists(dest_path):
                shutil.copy2(model_file, dest_path)
                print(f"📦 Copied {model_file} to {models_dir}/")
            else:
                print(f"ℹ️ {model_file} already exists in {models_dir}/")
        else:
            print(f"⚠️ {model_file} not found in current directory")

def create_directories():
    """Create necessary directories"""
    dirs = ['media', 'staticfiles', 'logs']
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"📁 Created {dir_name} directory")

def main():
    """Main setup function"""
    print("🚀 Setting up Face Prediction Django Application")
    print("=" * 50)
    
    # Check requirements
    check_python_version()
    
    # Setup virtual environment
    pip_cmd = setup_virtual_environment()
    
    # Install dependencies
    if not install_dependencies(pip_cmd):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create necessary directories
    create_directories()
    
    # Copy model files
    copy_model_files()
    
    # Setup database
    setup_database()
    
    # Collect static files
    collect_static_files()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("2. Run development server:")
    print("   python manage.py runserver")
    
    print("3. Open browser and go to:")
    print("   http://localhost:8000")
    
    print("\n🔑 Admin access:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   URL: http://localhost:8000/admin")
    
    print("\n🐳 For Docker deployment:")
    print("   docker-compose up --build")
    
    print("\n📚 For more information, see django_README.md")

if __name__ == "__main__":
    main() 