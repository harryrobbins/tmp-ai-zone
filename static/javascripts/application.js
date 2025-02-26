// Add JavaScript functionality for the Gov.UK components
(function () {
  // Initialize all GOV.UK components with data-module attributes
  window.GOVUKFrontend.initAll();

  // Initialize HMRC components if they exist
  if (window.HMRCFrontend && window.HMRCFrontend.initAll) {
    window.HMRCFrontend.initAll();
  }

  // Handle file upload
  const fileInput = document.getElementById('file-upload');
  if (fileInput) {
    fileInput.addEventListener('change', function(e) {
      if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        const fileSize = fileInput.files[0].size;

        // Convert bytes to MB for display
        const fileSizeMB = (fileSize / (1024 * 1024)).toFixed(2);

        // Logging for debug
        console.log(`File selected: ${fileName} (${fileSizeMB} MB)`);

        // Check file size
        if (fileSize > 100 * 1024 * 1024) { // 100MB in bytes
          alert('File size exceeds the maximum limit of 100MB.');
          fileInput.value = ''; // Clear the file input
        }
      }
    });
  }

  // Handle form submission
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', function(e) {
      // Validation could be added here
      const promptTextarea = document.getElementById('prompt');
      if (promptTextarea && promptTextarea.value.trim() === '') {
        e.preventDefault();
        alert('Please enter a prompt before submitting.');
      }
    });
  }
})();