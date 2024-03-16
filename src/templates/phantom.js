// app.js

document.getElementById('openWalletButton').addEventListener('click', function() {
    // Check if Phantom Wallet is installed
    if (window.solana && window.solana.isPhantom) {
        // Open Phantom Wallet extension
        window.solana.connect();
    } else {
        // Inform the user that Phantom Wallet is not installed
        alert('Phantom Wallet is not installed. Please install it to proceed.');
    }
});
