async function createWallet() {
    const response = await fetch('/api/create_wallet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: 1, username: 'Yansh' })
    });

    const data = await response.json();
    if (data.status === 'success') {
        document.getElementById('username').textContent = 'Yansh';
        alert('Wallet created successfully. Public Key: ' + data.public_key);
        localStorage.setItem('publicKey', data.public_key);
    } else {
        alert('Failed to create wallet.');
    }
}

async function updateBalances() {
    const publicKey = localStorage.getItem('publicKey');
    if (!publicKey) {
        await createWallet();
        return;
    }

    // Fetch SOL balance
    const solResponse = await fetch(`/api/get_balance?public_key=${publicKey}`);
    const solData = await solResponse.json();
    document.getElementById('sol-balance').textContent = `${solData.balance} SOL`;

    // Fetch $SLICKS balance - replace with actual endpoint when available
    // Example code for fetching balances from blockchain or database
    document.getElementById('slicks-balance').textContent = '0 SLICKS';  // Placeholder
}

function receive() {
    alert('Receive functionality under development.');
}

function swap() {
    alert('Swap functionality under development.');
}

function send() {
    alert('Send functionality under development.');
}

// On page load, update balances
window.onload = updateBalances;
