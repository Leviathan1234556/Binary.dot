function openContentInNewWindow(file) {
    window.open(file, '_blank');
  }

  async function connectMetaMask() {
    try {
      const provider = await detectEthereumProvider();

      if (provider) {
        await provider.request({method: 'eth_requestAccounts'});
        alert('Connected to MetaMask!');
        displayWalletInfo(); // Call function to display wallet information
      } else {
        alert('MetaMask not detected. Please install MetaMask and try again.');
      }
    } catch (error) {
      console.error(error);
    }
  }

  function displayWalletInfo() {
    // Modify content to display wallet information
    $('#content-heading').text('Wallet Information');
    $('.authentication-text').html('<p>Your wallet address: <span id="walletAddress"></span></p> To change account, open MetaMask, switch to your preferred account and refresh this tab ');

    // Get the current Ethereum address from MetaMask
    ethereum.request({method: 'eth_accounts'})
      .then((accounts) => {
        const walletAddress = accounts[0];
        $('#walletAddress').text(walletAddress);
      })
      .catch((error) => {
        console.error(error);
      });
  }