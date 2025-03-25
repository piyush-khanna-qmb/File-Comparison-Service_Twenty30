document.addEventListener('DOMContentLoaded', function() {
    const sourceFilename = document.getElementById('source-filename');
    const targetFilename = document.getElementById('target-filename');
    const sourcePreview = document.getElementById('source-preview');
    const targetPreview = document.getElementById('target-preview');
    const swapBtn = document.getElementById('swap-files');
    const mergeBtn = document.getElementById('merge-btn');
    const overwriteBtn = document.getElementById('overwrite-btn');
    const resultMessage = document.getElementById('result-message');

    // Swap files functionality
    swapBtn.addEventListener('click', function() {
        // Swap filename texts
        const tempFilename = sourceFilename.textContent;
        sourceFilename.textContent = targetFilename.textContent;
        targetFilename.textContent = tempFilename;

        // Swap preview contents
        const tempContent = sourcePreview.textContent;
        sourcePreview.textContent = targetPreview.textContent;
        targetPreview.textContent = tempContent;
    });

    // Helper function to show result message
    function showMessage(message, type) {
        resultMessage.textContent = message;
        resultMessage.className = `alert alert-${type}`;
        resultMessage.style.display = 'block';
    }

    // Common function for promotion
    function promoteFiles(mergeType) {
        fetch('/api/promote/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                source_file: sourceFilename.textContent,
                target_file: targetFilename.textContent,
                merge_type: mergeType
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showMessage(data.error, 'danger');
            } else {
                showMessage(data.message, 'success');
            }
        })
        .catch(error => {
            showMessage('An error occurred during promotion', 'danger');
            console.error('Error:', error);
        });
    }

    // Merge files functionality
    mergeBtn.addEventListener('click', function() {
        promoteFiles('merge');
    });

    // Overwrite files functionality
    overwriteBtn.addEventListener('click', function() {
        promoteFiles('overwrite');
    });
});