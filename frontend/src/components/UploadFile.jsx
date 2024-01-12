import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import $, { error, event } from 'jquery';

function UploadFile() {
    const [uploadedFile, setUploadedFile] = useState(null);
    const [convertedFileDownloadUrl, setConvertedFileDownloadUrl] = useState('');
    const [convertedFileName, setConvertedFileName] = useState('');
    const [imageSrc, setImageSrc] = useState('');
    const [targetConversions, setTargetConversions] = useState([]);
    const [selectedTargetMimetype, setSelectedTargetMimetype] = useState(null);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        const original_mimetype = file.name.split('.')[1];

        axios.get(
            'http://localhost:8000/backend/target_conversions',
            { params: { original_mimetype: original_mimetype } }
        )
            .then(response => {
                console.log(response);
                setUploadedFile(file);
                setTargetConversions(response.data.supported_mimetypes)
            })
            .catch(error => {
                console.log(error);
            });
    };

    const handleConversion = (event) => {
        event.preventDefault();

        const url = 'http://localhost:8000/backend/';
        const formData = new FormData();
        formData.append('original_file', uploadedFile);
        formData.append('converted_mimetype', selectedTargetMimetype);

        const headers = { 'X-CSRFTOKEN': getCookie('csrftoken') }

        fetch(url, { method: 'POST', headers: headers, body: formData })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.blob();
            })
            .then(b => {
                console.log(b);
                const blob = new Blob([b]);
                setConvertedFileDownloadUrl(window.URL.createObjectURL(blob));
                setConvertedFileName('converted_file.jpeg');
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
    };

    const handleCancelConversion = () => {
        setUploadedFile(null);
        setTargetConversions([]);
    }

    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    return (
        <div className="content">
            <div className="content content-full">
                <div className="d-flex flex-column justify-content-sm-between text-center">
                    <div className="flex-sm-fill font-size-h2 font-w400 text-center text-info">File Converter</div>
                    <div>Convert your files to any format</div>
                </div>
            </div>
            <div className="block block-rounded block-bordered">
                <form onSubmit={handleConversion}>
                    <div className="block-content">
                        {!uploadedFile &&
                            <div id="upload-file" className="text-center">
                                <label htmlFor="id_original_file" className="btn btn-hero-primary mb-3">
                                    <i className="fa fa-upload mr-1" aria-hidden="true"></i> Upload File
                                </label>
                                <input type="file" name="original_file" required id="id_original_file" onChange={handleFileChange} hidden />
                                <p>Upload your files here, 100MB maximum file size</p>
                                {uploadedFile && (<p>Selected file: {uploadedFile.name}</p>)}
                            </div>
                        }

                        {(convertedFileDownloadUrl.length == 0 && uploadedFile && targetConversions) &&
                            <div className='row push'>
                                <input type="hidden" name="csrfmiddlewaretoken" value={getCookie('csrftoken')} />
                                <div className='col-4'>{uploadedFile?.name}</div>
                                <div className='col-4'>{uploadedFile?.size} KB</div>
                                <div className='col-4'>
                                    <select className='form-control' onChange={(event) => setSelectedTargetMimetype(event.target.value)}>
                                        <option value="">Convert to ...</option>
                                        {targetConversions.map((option, index) => (
                                            <option key={index} value={option}>{option}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>
                        }

                        {
                            convertedFileDownloadUrl.length > 0 &&
                            <>
                                <a href={convertedFileDownloadUrl} className="btn btn-primary mr-1" download={convertedFileName}>
                                    <i className="fa fa-repeat"></i> Download
                                </a>
                            </>
                        }
                    </div>
                    <div className="block-content block-content-full block-content-sm bg-body-light text-right">
                        <button type="reset" className="btn btn-danger mr-1" onClick={handleCancelConversion}>
                            <i className="fa fa-repeat"></i> Cancel
                        </button>
                        <button type="submit" className="btn btn-success">
                            <i className="fa fa-check"></i> Convert
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default UploadFile;
