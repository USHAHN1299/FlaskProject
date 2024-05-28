# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file, session
# from werkzeug.utils import secure_filename
# from concurrent.futures import ProcessPoolExecutor
# import logging
# import time
# import numpy as np
# import math
# from auth_app import app as auth_app  # Importing the authentication app instance

# app = Flask(__name__)

# # Configure logging
# logging.basicConfig(
#     filename="app.log",
#     filemode='w',
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

# # Configuration for file upload
# UPLOAD_FOLDER = 'uploads'
# STATIC_FOLDER = 'static'
# ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

# app.config['UPLOAD_FOLDER'] = 'C:\\Users\\Usha.HN\\.spyder-py3\\Practice_Projects\\Cp_values_app\\Source\\uploads'
# app.config['STATIC_FOLDER'] = 'C:\\Users\\Usha.HN\\.spyder-py3\\Practice_Projects\\Cp_values_app\\Source\\static'


# r = 81
# A = math.pi * r ** 2

# # Function to check if the filename has a valid extension
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # Serve the HTML file with the upload form
# @app.route('/')
# def data_upload():
#     if 'username' in session:
#         return render_template('upload.html')
#     else:
#         return redirect(url_for('auth_app.index', message='You must login first'))

# # Handle the file upload
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'username' in session:
#         if 'file' not in request.files:
#             return 'No file part'
#         file = request.files['file']
#         if file.filename == '':
#             return 'No selected file'
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('calculate_cp_values', filename=filename))
#         else:
#             return 'Invalid file. Allowed file types are xls, xlsx.'
#     else:
#         return redirect(url_for('auth_app.index', message='You must login first'))

# # Function to calculate cp values
# def creating_dataframe(file):
#     logging.info("Starting main process")
#     try:
#         df = pd.read_excel(file)
#         logging.info("Excel file loaded successfully")
#     except Exception as e:
#         logging.error(f"Failed to load Excel file: {e}")
#         raise
#     return df

# def start_task(df, datapoints, rho):
#     with ProcessPoolExecutor() as executor:
#         args = [(rho, datapoint) for datapoint in datapoints]
#         cp_values = list(executor.map(calculate_cp, args))
#         df[f'Cp_Value_for_rho={rho}'] = cp_values
#         logging.info(f"Completed calculations for rho: {rho}")
#     return df

# def calculate_cp(args):
#     rho, (V, P) = args
#     try:
#         return P * 10**3 / (0.5 * rho * A * V**3)
#     except Exception as e:
#         logging.error(f"PID: {os.getpid()} - Calculating Cp for rho: {rho}, V: {V}, P: {P}")
#         logging.error(f"Failed to calculate Cp Value due to {e}")
#         raise

# # Route to display the cp values for selected rho
# @app.route('/calculate/<filename>', methods=['GET', 'POST'])
# def calculate_cp_values(filename):
#     if 'username' in session:
#         if request.method == 'POST':
#             start_time = time.perf_counter()
#             rho = float(request.form['rho'])
#             if rho < 0.9 or rho > 1.3:
#                 return 'rho value should be present between (0.9 , 1.3)'
            
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             if not os.path.exists(file_path):
#                 return f"File {filename} not found", 404
            
#             df = creating_dataframe(file_path)
#             datapoints = df[['V', 'P']].values.tolist()
#             result = start_task(df, datapoints, rho)
#             # Ensure the specific column for the selected rho exists
#             column_name = f'Cp_Value_for_rho={rho}'
#             if column_name not in result.columns:
#                 result[column_name] = [calculate_cp((rho, (V, P))) for V, P in datapoints]
#             max_cp = max(result[column_name])
#             try:
#                 # Plot the graph
#                 # plt.figure(figsize=(10, 6))
#                 # plt.plot(result['V'], result[column_name], marker='o', linestyle='-', color='b')
#                 # plt.title(f'Wind Speed vs CP Values for Rho={rho}')
#                 # plt.xlabel('Wind Speed')
#                 # plt.ylabel('CP Value')
#                 # plt.grid(True)
#                 # plot_filename = os.path.join(app.config['STATIC_FOLDER'], 'plot.png')
#                 # plt.savefig(plot_filename)
#                 # plt.show()
#                 # plt.close()
                
#                 # Plotting with annotation for max value
#                 plt.figure(figsize=(10, 8))
#                 plt.plot(result['V'], result[f'Cp_Value_for_rho={rho}'], marker='o', linestyle='-', color='b', label='CP Values')
#                 max_idx = np.argmax(result[f'Cp_Value_for_rho={rho}'])
#                 max_value = result[f'Cp_Value_for_rho={rho}'][max_idx]
#                 max_speed = result['V'][max_idx]
#                 plt.annotate(f'Max CP Value: {max_value:.2f}', xy=(max_speed, max_value), xytext=(max_speed + 1, max_value + 0.01),
#                              arrowprops=dict(facecolor='red', shrink=0.05))
#                 plt.title(f'Wind Speed vs CP Values for Rho={rho}')
#                 plt.xlabel('Wind Speed')
#                 plt.ylabel('CP Value')
#                 plt.grid(True)
#                 plt.legend()
#                 plot_filename = 'plot.png'
#                 plot_filepath = os.path.join(app.config['STATIC_FOLDER'], plot_filename)
#                 plt.savefig(plot_filepath)
#                 logging.info(f"Plot saved to {plot_filename}")
        
#                 # Save the calculated results in an Excel sheet
#                 output_file = 'output.xlsx'
#                 excel_file = os.path.join(app.config['UPLOAD_FOLDER'], output_file)
#                 result.to_excel(excel_file, index=False)
#                 logging.info(f"DataFrame successfully saved to {output_file}")
        
#                 end_time = time.perf_counter()
#                 logging.info(f"Total time taken {round(end_time - start_time, 2)} seconds")
#                 return render_template('results.html', rho=rho, plot_filename=plot_filename, output_filename=output_file, maximum_Cp=max_cp)
#             except Exception as e:
#                 logging.error(f"Error processing data: {e}")
#                 return f"Error processing data: {e}", 500
#         else:
#             return render_template('calculate.html', filename=filename)
#     else:
#         return redirect(url_for('auth_app.index', message='You must login first'))

# @app.route('/plot/<filename>')
# def plot(filename):
#     return send_from_directory(app.config['STATIC_FOLDER'], filename)

# # Route to download the uploaded and calculated files
# @app.route('/download/<filename>')
# def download_files(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# # Route to download the plot
# @app.route('/download_plot/<filename>')
# def download_plot(filename):
#     plot_path = os.path.join(app.config['STATIC_FOLDER'], filename)
#     return send_file(plot_path, as_attachment=True)

# if __name__ == '__main__':
#     # if not os.path.exists(app.config['UPLOAD_FOLDER']):
#     #     os.makedirs(app.config['UPLOAD_FOLDER'])
#     app.run()


# data_app.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, send_file, session
from werkzeug.utils import secure_filename
from concurrent.futures import ProcessPoolExecutor
import logging
import time
import numpy as np
import math

data_bp = Blueprint('data_app', __name__, template_folder='templates', static_folder='static')

# Configure logging
logging.basicConfig(
    filename="app.log",
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configuration for file upload
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

data_bp.config = {}
data_bp.config['UPLOAD_FOLDER'] = 'C:\\Users\\Usha.HN\\.spyder-py3\\Practice_Projects\\Flask_Project\\data_app\\uploads'
data_bp.config['STATIC_FOLDER'] = 'C:\\Users\\Usha.HN\\.spyder-py3\\Practice_Projects\\Flask_Project\\data_app\\static'

r = 81
A = math.pi * r ** 2

# Function to check if the filename has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Serve the HTML file with the upload form
@data_bp.route('/')
def data_upload():
    if 'username' in session:
        return render_template('upload.html')
    else:
        return redirect(url_for('auth_bp.index', message='You must login first'))

# Handle the file upload
@data_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'username' in session:
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(data_bp.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('data_app.calculate_cp_values', filename=filename))
        else:
            return 'Invalid file. Allowed file types are xls, xlsx.'
    else:
        return redirect(url_for('auth_bp.index', message='You must login first'))

# Function to calculate cp values
def creating_dataframe(file):
    logging.info("Starting main process")
    try:
        df = pd.read_excel(file)
        logging.info("Excel file loaded successfully")
    except Exception as e:
        logging.error(f"Failed to load Excel file: {e}")
        raise
    return df

def start_task(df, datapoints, rho):
    with ProcessPoolExecutor() as executor:
        args = [(rho, datapoint) for datapoint in datapoints]
        cp_values = list(executor.map(calculate_cp, args))
        df[f'Cp_Value_for_rho={rho}'] = cp_values
        logging.info(f"Completed calculations for rho: {rho}")
    return df

def calculate_cp(args):
    rho, (V, P) = args
    try:
        return P * 10**3 / (0.5 * rho * A * V**3)
    except Exception as e:
        logging.error(f"PID: {os.getpid()} - Calculating Cp for rho: {rho}, V: {V}, P: {P}")
        logging.error(f"Failed to calculate Cp Value due to {e}")
        raise

# Route to display the cp values for selected rho
@data_bp.route('/calculate/<filename>', methods=['GET', 'POST'])
def calculate_cp_values(filename):
    if 'username' in session:
        if request.method == 'POST':
            start_time = time.perf_counter()
            rho = float(request.form['rho'])
            if rho < 0.9 or rho > 1.3:
                return 'rho value should be present between (0.9 , 1.3)'
            
            file_path = os.path.join(data_bp.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(file_path):
                return f"File {filename} not found", 404
            
            df = creating_dataframe(file_path)
            datapoints = df[['V', 'P']].values.tolist()
            result = start_task(df, datapoints, rho)
            # Ensure the specific column for the selected rho exists
            column_name = f'Cp_Value_for_rho={rho}'
            if column_name not in result.columns:
                result[column_name] = [calculate_cp((rho, (V, P))) for V, P in datapoints]
            max_cp = max(result[column_name])
            try:
                # Plot the graph
                # plt.figure(figsize=(10, 6))
                # plt.plot(result['V'], result[column_name], marker='o', linestyle='-', color='b')
                # plt.title(f'Wind Speed vs CP Values for Rho={rho}')
                # plt.xlabel('Wind Speed')
                # plt.ylabel('CP Value')
                # plt.grid(True)
                # plot_filename = os.path.join(data_bp.config['STATIC_FOLDER'], 'plot.png')
                # plt.savefig(plot_filename)
                # plt.show()
                # plt.close()
                
                # Plotting with annotation for max value
                plt.figure(figsize=(10, 8))
                plt.plot(result['V'], result[f'Cp_Value_for_rho={rho}'], marker='o', linestyle='-', color='b', label='CP Values')
                max_idx = np.argmax(result[f'Cp_Value_for_rho={rho}'])
                max_value = result[f'Cp_Value_for_rho={rho}'][max_idx]
                max_speed = result['V'][max_idx]
                plt.annotate(f'Max CP Value: {max_value:.2f}', xy=(max_speed, max_value), xytext=(max_speed + 1, max_value + 0.01),
                             arrowprops=dict(facecolor='red', shrink=0.05))
                plt.title(f'Wind Speed vs CP Values for Rho={rho}')
                plt.xlabel('Wind Speed')
                plt.ylabel('CP Value')
                plt.grid(True)
                plt.legend()
                plot_filename = 'plot.png'
                plot_filepath = os.path.join(data_bp.config['STATIC_FOLDER'], plot_filename)
                plt.savefig(plot_filepath)
                logging.info(f"Plot saved to {plot_filename}")
        
                # Save the calculated results in an Excel sheet
                output_file = 'output.xlsx'
                excel_file = os.path.join(data_bp.config['UPLOAD_FOLDER'], output_file)
                result.to_excel(excel_file, index=False)
                logging.info(f"DataFrame successfully saved to {output_file}")
        
                end_time = time.perf_counter()
                logging.info(f"Total time taken {round(end_time - start_time, 2)} seconds")
                return render_template('results.html', rho=rho, plot_filename=plot_filename, output_filename=output_file, maximum_Cp=max_cp)
            except Exception as e:
                logging.error(f"Error processing data: {e}")
                return f"Error processing data: {e}", 500
        else:
            return render_template('calculate.html', filename=filename)
    else:
        return redirect(url_for('auth_bp.index', message='You must login first'))

@data_bp.route('/plot/<filename>')
def plot(filename):
    return send_from_directory(data_bp.config['STATIC_FOLDER'], filename)

# Route to download the uploaded and calculated files
@data_bp.route('/download/<filename>')
def download_files(filename):
    return send_from_directory(data_bp.config['UPLOAD_FOLDER'], filename)

# Route to download the plot
@data_bp.route('/download_plot/<filename>')
def download_plot(filename):
    plot_path = os.path.join(data_bp.config['STATIC_FOLDER'], filename)
    return send_file(plot_path, as_attachment=True)
