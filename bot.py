from web3 import Web3
from colorama import init, Fore, Style
import sys
import time

# Initialize colorama
init(autoreset=True)

# Display header information
def display_header():
    header_text = """
    ===============================
    Auto Daily Claim $RWT Humanity Protocol
    Bot created by: https://t.me/AirdropInsiderID
    ===============================
    """
    print(Fore.CYAN + Style.BRIGHT + header_text + "\n")

# Blockchain setup and connection
def setup_blockchain_connection(rpc_url):
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if web3.is_connected():
        print(Fore.GREEN + "Connected to Humanity Protocol")
    else:
        print(Fore.RED + "Connection failed.")
        sys.exit(1)  # Exit if connection fails
    return web3

# Load private keys from a file
def load_private_keys(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Check if reward needs to be claimed
def claim_rewards(private_key, web3, contract):
    try:
        account = web3.eth.account.from_key(private_key)
        sender_address = account.address
        genesis_claimed = contract.functions.userGenesisClaimStatus(sender_address).call()
        current_epoch = contract.functions.currentEpoch().call()
        buffer_amount, claim_status = contract.functions.userClaimStatus(sender_address, current_epoch).call()

        if genesis_claimed and not claim_status:
            print(Fore.GREEN + f"Claiming reward for address: {sender_address} (Genesis reward claimed).")
            process_claim(sender_address, private_key, web3, contract)
        elif not genesis_claimed:
            print(Fore.GREEN + f"Claiming reward for address: {sender_address} (Genesis reward not claimed).")
            process_claim(sender_address, private_key, web3, contract)
        else:
            print(Fore.YELLOW + f"Reward already claimed for address: {sender_address} in epoch {current_epoch}. Skipping.")

    except Exception as e:
        handle_error(e, sender_address)

# Handle specific errors for clarity
def handle_error(e, address):
    error_message = str(e)
    if "Rewards: user not registered" in error_message:
        print(Fore.RED + f"Error: User {address} is not registered.")
    else:
        print(Fore.RED + f"Error claiming reward for {address}: {error_message}")

# Process the claim reward transaction
def process_claim(sender_address, private_key, web3, contract):
    try:
        gas_amount = contract.functions.claimReward().estimate_gas({
            'chainId': web3.eth.chain_id,
            'from': sender_address,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(sender_address)
        })
        transaction = contract.functions.claimReward().build_transaction({
            'chainId': web3.eth.chain_id,
            'from': sender_address,
            'gas': gas_amount,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(sender_address)
        })
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(Fore.GREEN + f"Transaction successful for {sender_address} with hash: {web3.to_hex(tx_hash)}")

    except Exception as e:
        print(Fore.RED + f"Error processing claim for {sender_address}: {str(e)}")

# Main execution
if __name__ == "__main__":
    display_header()
    rpc_url = 'https://rpc.testnet.humanity.org'
    web3 = setup_blockchain_connection(rpc_url)
    
    contract_address = '0xa18f6FCB2Fd4884436d10610E69DB7BFa1bFe8C7'
    contract_abi = [{"inputs":[],"name":"AccessControlBadConfirmation","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"bytes32","name":"neededRole","type":"bytes32"}],"name":"AccessControlUnauthorizedAccount","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"bool","name":"bufferSafe","type":"bool"}],"name":"ReferralRewardBuffered","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"enum IRewards.RewardType","name":"rewardType","type":"uint8"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardClaimed","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":True,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":True,"internalType":"address","name":"account","type":"address"},{"indexed":True,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimBuffer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"currentEpoch","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cycleStartTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"vcContract","type":"address"},{"internalType":"address","name":"tkn","type":"address"}],"name":"init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"callerConfirmation","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"startTimestamp","type":"uint256"}],"name":"start","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userBuffer","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"epochID","type":"uint256"}],"name":"userClaimStatus","outputs":[{"components":[{"internalType":"uint256","name":"buffer","type":"uint256"},{"internalType":"bool","name":"claimStatus","type":"bool"}],"internalType":"struct IRewards.UserClaim","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userGenesisClaimStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]  # Place the ABI here
    contract = web3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=contract_abi)

    # Infinite loop to run every 6 hours
    while True:
        private_keys = load_private_keys('private_keys.txt')
        for private_key in private_keys:
            claim_rewards(private_key, web3, contract)
        
        print(Fore.CYAN + "Waiting for 6 hours before the next run...")
        time.sleep(6 * 60 * 60)  # For testing purposes, you may want to reduce this time
