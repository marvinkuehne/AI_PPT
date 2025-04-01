import { useRef, useState, useEffect } from 'react';
import {BACKEND_URL} from "../global_varaibles.ts";

export default function GeneratePptPage() {
  const [imageData, setImageData] = useState(null);
  const [status, setStatus] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const fileInputRef = useRef(null);
  const dropAreaRef = useRef(null);
  const previewRef = useRef(null);

  useEffect(() => {
    const handlePaste = (e) => {
      const items = e.clipboardData.items;
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
          const blob = items[i].getAsFile();
          displayImage(blob);
          break;
        }
      }
    };

    const preventDefaults = (e) => {
      e.preventDefault();
      e.stopPropagation();
    };

    const handleDrop = (e) => {
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        displayImage(files[0]);
      }
    };

    document.addEventListener('paste', handlePaste);
    const dropArea = dropAreaRef.current;
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
      dropArea.addEventListener(event, preventDefaults, false);
    });
    dropArea.addEventListener('drop', handleDrop);

    return () => {
      document.removeEventListener('paste', handlePaste);
      ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
        dropArea.removeEventListener(event, preventDefaults);
      });
      dropArea.removeEventListener('drop', handleDrop);
    };
  }, []);

  const displayImage = (blob) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const base64 = e.target.result;
      const img = new Image();
      img.src = base64;
      img.className = 'max-w-full max-h-[300px] mx-auto';
      previewRef.current.innerHTML = '';
      previewRef.current.appendChild(img);
      setImageData(base64.split(',')[1]);
      setStatus('Ready to convert');
    };
    reader.readAsDataURL(blob);
  };

  const handleConvert = async () => {
    if (!imageData) return;
    setIsProcessing(true);
    setStatus('Processing...');
    try {
      const response = await fetch(BACKEND_URL + '/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: imageData }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'presentation.pptx';
        document.body.appendChild(a);
        a.click();
        URL.revokeObjectURL(url);
        setStatus('Conversion successful!');
      } else {
        const error = await response.text();
        setStatus(`Error: ${error}`);
      }
    } catch (err) {
      setStatus(`Error: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 font-sans">
      <h1 className="text-2xl font-bold mb-4">Image to PowerPoint Converter</h1>
      <div
        ref={dropAreaRef}
        className="border-2 border-dashed border-gray-400 p-10 text-center my-6"
      >
        <p>Drag & drop image here or paste (Ctrl+V)</p>
        <input
          type="file"
          accept="image/*"
          ref={fileInputRef}
          style={{ display: 'none' }}
        />
      </div>
      <div ref={previewRef} className="text-center my-6"></div>
      <button
        className="px-6 py-3 bg-green-600 text-white text-lg rounded disabled:bg-gray-400"
        onClick={handleConvert}
        disabled={!imageData || isProcessing}
      >
        Convert to PowerPoint
      </button>
      <div className="mt-4 text-gray-600">{status}</div>
    </div>
  );
}