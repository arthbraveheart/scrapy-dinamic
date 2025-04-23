const submitButton = document.getElementById ('submitButton');
const statusModal = document.getElementById ('statusModal');
let checkInterval = null;

document.addEventListener ('DOMContentLoaded' , function () {
    checkSpiderStatus ();
});

document.getElementById ('spiderForm').addEventListener ('submit' , function (e) {
    e.preventDefault ();
    const modal = new bootstrap.Modal (document.getElementById ('statusModal'));
    modal.show (); // Show modal on form submission

    fetch ("{% url 'run-spider' %}" , {
        method: 'POST' ,
        headers: {'X-CSRFToken': '{{ csrf_token }}'} ,
        body: new FormData (this)
    }).then (() => {
        checkSpiderStatus ();
    }).catch (error => {
        const statusTitle = document.getElementById ('statusTitle');
        const statusMessage = document.getElementById ('statusMessage');
        statusTitle.textContent = 'Error!';
        statusMessage.textContent = 'Failed to start spider: ' + error;
    });
});

function checkSpiderStatus () {
    fetch (`{% url 'spider-status' %}?t=${Date.now ()}`)
        .then (response => {
            if (!response.ok) throw Error ('Network error');
            return response.json ();
        })
        .then (data => {
            submitButton.disabled = data.status === 'running';
            // Add visual feedback
            submitButton.innerHTML = data.status === 'running'
                ? '<span class="spinner-border spinner-border-sm" role="status"></span> Running...'
                : 'Run Spider';
        })
        .catch (console.error);
}

// Handle modal show/hide events for polling
statusModal.addEventListener ('show.bs.modal' , function () {
    const statusTitle = document.getElementById ('statusTitle');
    const statusMessage = document.getElementById ('statusMessage');
    const progressBar = document.getElementById ('progressBar');
    const progressStats = document.getElementById ('progressStats');

    // Initialize UI
    statusTitle.textContent = 'Processing...';
    statusMessage.textContent = 'Checking spider status...';
    progressBar.style.width = '0%';
    progressBar.setAttribute ('aria-valuenow' , 0);
    progressBar.classList.add ('indeterminate');

    let attempts = 0;
    const MAX_ATTEMPTS = 2000;

    function checkStatus () {
        attempts++;
        if (attempts > MAX_ATTEMPTS) {
            clearInterval (checkInterval);
            statusTitle.textContent = 'Timeout';
            statusMessage.textContent = 'Spider is taking too long. Check status later.';
            return;
        }

        fetch (`{% url 'spider-status' %}?t=${Date.now ()}`)
            .then (response => {
                if (!response.ok) throw Error ('Network error');
                return response.json ();
            })
            .then (data => {
                statusMessage.textContent = data.message || data.status;

                if (data.progress) {
                    const {percentage , completed , total} = data.progress;
                    progressStats.textContent = `${completed} / ${total} EANs processed`;

                    if (data.status === 'running' && total > 0) {
                        progressBar.style.width = `${percentage}%`;
                        progressBar.setAttribute ('aria-valuenow' , percentage);
                        if (percentage > 0) progressBar.classList.remove ('indeterminate');
                    }
                }

                if (data.status === 'completed') {
                    statusTitle.textContent = 'Completed!';
                    progressBar.style.width = '100%';
                    progressBar.setAttribute ('aria-valuenow' , 100);
                    clearInterval (checkInterval);
                } else if (data.status.startsWith ('failed') || data.status.startsWith ('error')) {
                    statusTitle.textContent = 'Failed!';
                    clearInterval (checkInterval);
                }
            })
            .catch (error => {
                console.error ('Polling error:' , error);
                statusMessage.textContent = 'Connection error - retrying...';
            });
    }

    // Immediate check and then every 2 seconds
    checkStatus ();
    checkInterval = setInterval (checkStatus , 2000);
});

statusModal.addEventListener ('hidden.bs.modal' , function () {
    if (checkInterval) {
        clearInterval (checkInterval);
        checkInterval = null;
    }
});