import { useRef, useState, useEffect } from 'react';
import { GLOBAL } from "../global_varaibles.ts";
import Page from "../components/Page.tsx";

const DRAG_EVENTS = ['dragenter', 'dragover', 'dragleave', 'drop'] as const;

export default function ConverterPage() {
    const [imageData, setImageData] = useState<string | null>(null);
    const [status, setStatus] = useState<string>('');
    const [isProcessing, setIsProcessing] = useState<boolean>(false);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const dropAreaRef = useRef<HTMLDivElement>(null);
    const previewRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handlePaste = (e: ClipboardEvent) => {
            const items = e.clipboardData?.items;
            if (!items) return;
            for (let i = 0; i < items.length; i++) {
                if (items[i].type.startsWith('image/')) {
                    const blob = items[i].getAsFile();
                    if (blob) displayImage(blob);
                    break;
                }
            }
        };

        // Accept a generic Event so we can listen for multiple drag events
        const preventDefaults = (e: Event) => {
            e.preventDefault();
            e.stopPropagation();
        };

        const handleDrop = (e: Event) => {
            preventDefaults(e);
            const dragEvent = e as DragEvent;
            const files = dragEvent.dataTransfer?.files;
            if (files && files.length > 0) {
                displayImage(files[0]);
            }
        };

        document.addEventListener('paste', handlePaste as EventListener);
        const dropArea = dropAreaRef.current;
        if (dropArea) {
            DRAG_EVENTS.forEach((event) => {
                dropArea.addEventListener(event, preventDefaults);
            });
            dropArea.addEventListener('drop', handleDrop as EventListener);
        }

        return () => {
            document.removeEventListener('paste', handlePaste as EventListener);
            if (dropArea) {
                DRAG_EVENTS.forEach((event) => {
                    dropArea.removeEventListener(event, preventDefaults);
                });
                dropArea.removeEventListener('drop', handleDrop as EventListener);
            }
        };
    }, []);

    const displayImage = (blob: Blob) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const base64 = e.target?.result as string;
            const img = new Image();
            img.src = base64;
            img.className = 'max-w-full max-h-[300px] mx-auto';
            if (previewRef.current) {
                previewRef.current.innerHTML = '';
                previewRef.current.appendChild(img);
            }
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
            const response = await fetch(`${GLOBAL.BACKEND_URL}/convert`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: imageData }),
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'result.pptx';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                setStatus('Conversion successful!');
            } else {
                const error = await response.text();
                setStatus(`Error: ${error}`);
            }
        } catch (err: any) {
            setStatus(`Error: ${err.message}`);
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <Page title='Converter'>
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
        </Page>
    );
}