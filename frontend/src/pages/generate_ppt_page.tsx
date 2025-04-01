function GeneratePptPage() {
  return (
      <div>
        <h1>Image to PowerPoint Converter</h1>
        <div id="drop-area">
          <p>Drag & drop image here or paste (Ctrl+V)</p>
          <input type="file" id="file-input" accept="image/*" className="p-4 hidden" />
        </div>
        <div id="preview"></div>
        <button id="convert-btn" disabled>Convert to PowerPoint</button>
        <div id="status"></div>
      </div>
  );
}

export default GeneratePptPage;