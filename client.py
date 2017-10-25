import requests
import json
from pprint import pprint

BASE_URL = 'http://localhost:5279/lbryapi'

def _request(method, **kwargs):
    params = {}
    for k, v in kwargs.items():
        params[k] = v
    data = json.dumps({'method': method, 'params': params})
    res = requests.post(BASE_URL, data=data)
    res.raise_for_status
    result = res.json()
    if 'error' in result:
        code = result['error']['code']
        msg = result['error']['message']
        raise Exception(code, msg)
    return result['result']

def channel_list_mine():
    """Get my channels

    Returns:
        (list) ClaimDict
    """
    res = _request('channel_list_mine')
    return res

def channel_new(name, amount):
    """Generate a publisher key and create a new certificate claim

    Args:
        'channel_name': (str) '@' prefixed name
        'amount': (float) amount to claim name

    Returns:
        (dict) Dictionary containing result of the claim
        {
            'tx' : (str) hex encoded transaction
            'txid' : (str) txid of resulting claim
            'nout' : (int) nout of the resulting claim
            'fee' : (float) fee paid for the claim transaction
            'claim_id' : (str) claim ID of the resulting claim
        }
    """
    if name[0] != '@':
        name = '@' + name
    if not isinstance(amount, float):
        amount = float(amount)

    res = _request('channel_new', channel_name=name, amount=amount)
    return res['result']['claim_id']

def claim_abandon(claim_id):
    """Abandon a name and reclaim credits from the claim

    Args:
        'claim_id': (str) claim_id of claim
    Return:
        (dict) Dictionary containing result of the claim
        {
            txid : (str) txid of resulting transaction
            fee : (float) fee paid for the transaction
        }
    """
    res = _request('claim_abandon', claim_id=claim_id)
    print(res)
    return res

def claim_list(name):
    """Get Claims for a name
    
    Arguments:
        name {str} -- search for claims on this name
    
    Returns:
        (dict) State of claims assigned for the name
    {
        'claims': (list) list of claims for the name
        [
            {
            'amount': (float) amount assigned to the claim
            'effective_amount': (float) total amount assigned to the claim,
                                including supports
            'claim_id': (str) claim ID of the claim
            'height': (int) height of block containing the claim
            'txid': (str) txid of the claim
            'nout': (int) nout of the claim
            'supports': (list) a list of supports attached to the claim
            'value': (str) the value of the claim
            },
        ]
        'supports_without_claims': (list) supports without any claims attached to them
        'last_takeover_height': (int) the height of last takeover for the name
    }
    """
    res = _request('claim_list', name=name)
    return res

def claim_list_mine():
    """List my name claims
    Returns
    (list) List of name claims owned by user
    [
        {
            'address': (str) address that owns the claim
            'amount': (float) amount assigned to the claim
            'blocks_to_expiration': (int) number of blocks until it expires
            'category': (str) "claim", "update" , or "support"
            'claim_id': (str) claim ID of the claim
            'confirmations': (int) number of blocks of confirmations for the claim
            'expiration_height': (int) the block height which the claim will expire
            'expired': (bool) true if expired, false otherwise
            'height': (int) height of the block containing the claim
            'is_spent': (bool) true if claim is abandoned, false otherwise
            'name': (str) name of the claim
            'txid': (str) txid of the cliam
            'nout': (int) nout of the claim
            'value': (str) value of the claim
        },
   ]
   """
   res = _request('claim_list_mine')
   return res

def claim_new_support(name, claim_id, amount):
    """Support a claim name

    Args:
        'name': (str) Name of claim
        'claim_id': (str) claim ID of claim to support
        'amount': (float) amount to support by

    Return:
        (dict) Dictionary containing result of the claim
        {
            txid : (str) txid of resulting support claim
            nout : (int) nout of the resulting support claim
            fee : (float) fee paid for the transaction
        }
    """
    if not isinstance(amount, float):
        amount = float(amount)
    res = _request('claim_new_support', name, claim_id, amount)
    return res

def claim_show(name, txid=None, nout=None, claim_id=None):
    """ Resolve claim info from a LBRY name

    Args:
        'name': (str) name to look up, do not include lbry:// prefix
        'txid'(optional): (str) if specified, look for claim with this txid
        'nout'(optional): (int) if specified, look for claim with this nout
        'claim_id'(optional): (str) if specified, look for claim with this claim_id
    Returns:
        (dict) Dictionary containing claim info, (bool) false if claim is not
            resolvable

        {
            'txid': (str) txid of claim
            'nout': (int) nout of claim
            'amount': (float) amount of claim
            'value': (str) value of claim
            'height' : (int) height of claim takeover
            'claim_id': (str) claim ID of claim
            'supports': (list) list of supports associated with claim
        }
    """

def descriptor_get(sd_hash, timeout=None, payment_rate_manager=None):
    """Download and return a sd blob

    Args:
    'sd_hash': (str) hash of sd blob
    'timeout'(optional): (int) timeout in number of seconds
    'payment_rate_manager'(optional): (str) if not given the default payment rate manager
                                     will be used. supported alternative rate managers:
                                     only-free

    Returns
        (str) Success/Fail message or (dict) decoded data
    """
    res = _request('descriptor_get', sd_hash, timeout, payment_rate_manager)
    return res

def file_delete(name=None, sd_hash=None, file_hash=None, stream_hash=None, claim_id=None, outpoint=None, rowid=None, delete_target_file=None):
    """Delete a lbry file

    Args:
        'name' (optional): (str) delete file by lbry name,
        'sd_hash' (optional): (str) delete file by sd hash,
        'file_name' (optional): (str) delete file by the name in the downloads folder,
        'stream_hash' (optional): (str) delete file by stream hash,
        'claim_id' (optional): (str) delete file by claim ID,
        'outpoint' (optional): (str) delete file by claim outpoint,
        'rowid': (optional): (int) delete file by rowid in the file manager
        'delete_target_file' (optional): (bool) delete file from downloads folder,
                                        defaults to true if false only the blobs and
                                        db entries will be deleted
    Returns:
        (bool) true if deletion was successful
    """
    res = _request('file_delete', name, sd_hash, file_hash, stream_hash, claim_id, outpoint, rowid, delete_target_file)
    return res

def file_list(**kwargs):
    """List files limited by optional filters

    Args:
        'name' (optional): (str) filter files by lbry name,
        'sd_hash' (optional): (str) filter files by sd hash,
        'file_name' (optional): (str) filter files by the name in the downloads folder,
        'stream_hash' (optional): (str) filter files by stream hash,
        'claim_id' (optional): (str) filter files by claim id,
        'outpoint' (optional): (str) filter files by claim outpoint,
        'rowid' (optional): (int) filter files by internal row id,
        'full_status': (optional): (bool) if true populate the 'message' and 'size' fields

    Returns:
        (list) List of files

        [
            {
                'completed': (bool) true if download is completed,
                'file_name': (str) name of file,
                'download_directory': (str) download directory,
                'points_paid': (float) credit paid to download file,
                'stopped': (bool) true if download is stopped,
                'stream_hash': (str) stream hash of file,
                'stream_name': (str) stream name ,
                'suggested_file_name': (str) suggested file name,
                'sd_hash': (str) sd hash of file,
                'name': (str) name claim attached to file
                'outpoint': (str) claim outpoint attached to file
                'claim_id': (str) claim ID attached to file,
                'download_path': (str) download path of file,
                'mime_type': (str) mime type of file,
                'key': (str) key attached to file,
                'total_bytes': (int) file size in bytes, None if full_status is false
                'written_bytes': (int) written size in bytes
                'message': (str), None if full_status is false
                'metadata': (dict) Metadata dictionary
            },
        ]
    """
    res = _request('file_list', **kwargs)
    return res

def file_set_status(status, name=None, sd_hash=None, file_name=None):
    """Start or stop downloading a file

    Args:
        'status': (str) "start" or "stop"
        'name' (optional): (str) start file by lbry name,
        'sd_hash' (optional): (str) start file by the hash in the name claim,
        'file_name' (optional): (str) start file by its name in the downloads folder,
    Returns:
        (str) Confirmation message
    """



def get(uri, file_name=None, timeout=None, download_directory=None):
    """Download stream from a LBRY name.

    Args:
        'uri': (str) lbry uri to download
        'file_name'(optional): (str) a user specified name for the downloaded file
        'timeout'(optional): (int) download timeout in number of seconds
        'download_directory'(optional): (str) path to directory where file will be saved
    Returns:
        (dict) Dictionary containing information about the stream
        {
            'completed': (bool) true if download is completed,
            'file_name': (str) name of file,
            'download_directory': (str) download directory,
            'points_paid': (float) credit paid to download file,
            'stopped': (bool) true if download is stopped,
            'stream_hash': (str) stream hash of file,
            'stream_name': (str) stream name,
            'suggested_file_name': (str) suggested file name,
            'sd_hash': (str) sd hash of file,
            'name': (str) name claim attached to file
            'outpoint': (str) claim outpoint attached to file
            'claim_id': (str) claim ID attached to file,
            'download_path': (str) download path of file,
            'mime_type': (str) mime type of file,
            'key': (str) key attached to file,
            'total_bytes': (int) file size in bytes, None if full_status is false
            'written_bytes': (int) written size in bytes
            'message': (str), None if full_status is false
            'metadata': (dict) Metadata dictionary
        }
    """

def get_availability(uri, sd_timeout=None, peer_timeout=None):
    """Get stream availability for lbry uri

    Args:
        'uri' : (str) lbry uri
        'sd_timeout' (optional): (int) sd blob download timeout
        'peer_timeout' (optional): (int) how long to look for peers

    Returns:
        (float) Peers per blob / total blobs
    """

def peer_list(blob_hash, timeout=None):
    """Get peers for blob hash

    Args:
        'blob_hash': (str) blob hash
        'timeout'(optional): (int) peer search timeout in seconds
    Returns:
        (list) List of contacts
    """
    res = _request('peer_list', blob_hash=blob_hash, timeout=timeout)
    return res

def publish(name, bid, metadata=None, **kwargs):
    """Make a new name claim and publish associated data to lbrynet.

    Updates over existing claim if user already has a claim for name.

    Fields required in the final Metadata are:
        'title'
        'description'
        'author'
        'language'
        'license',
        'nsfw'

    Metadata can be set by either using the metadata argument or by setting individual arguments
    fee, title, description, author, language, license, license_url, thumbnail, preview, nsfw,
    or sources. Individual arguments will overwrite the fields specified in metadata argument.

    Args:
        'name': (str) name to be claimed
        'bid': (float) amount of credits to commit in this claim,
        'metadata'(optional): (dict) Metadata to associate with the claim.
        'file_path'(optional): (str) path to file to be associated with name. If provided,
                                a lbry stream of this file will be used in 'sources'.
                                If no path is given but a metadata dict is provided, the source
                                from the given metadata will be used.
        'fee'(optional): (dict) Dictionary representing key fee to download content:
                          {currency_symbol: {'amount': float, 'address': str, optional}}
                          supported currencies: LBC, USD, BTC
                          If an address is not provided a new one will be automatically
                          generated. Default fee is zero.
        'title'(optional): (str) title of the file
        'description'(optional): (str) description of the file
        'author'(optional): (str) author of the file
        'language'(optional): (str), language code
        'license'(optional): (str) license for the file
        'license_url'(optional): (str) URL to license
        'thumbnail'(optional): (str) thumbnail URL for the file
        'preview'(optional): (str) preview URL for the file
        'nsfw'(optional): (bool) True if not safe for work
        'sources'(optional): (dict){'lbry_sd_hash':sd_hash} specifies sd hash of file
        'channel_name' (optional): (str) name of the publisher channel

    Returns:
        (dict) Dictionary containing result of the claim
        {
            'tx' : (str) hex encoded transaction
            'txid' : (str) txid of resulting claim
            'nout' : (int) nout of the resulting claim
            'fee' : (float) fee paid for the claim transaction
            'claim_id' : (str) claim ID of the resulting claim
        }
    """
    if metadata is None:
        metadata = {}
    fields = ['title', 'description', 'author', 'language', 'license', 'nsfw']
    for f in fields:
        if kwargs.get(f) is None and metadata.get(f) is None:
            msg = '{} is a required field for publishing. Please include it as a keyword arg or within metadata'
            raise Exception(msg)

    res = _request('publish', name, bid, metadata, **kwargs)
    return res

def reflect(sd_hash):
    """Reflect a stream

    Args:
        'sd_hash': (str) sd_hash of lbry file
    Returns:
        (bool) true if successful
    """
    res = _request('reflect', sd_hash=sd_hash)



def resolve(uri):
    """Resolve a LBRY URI

    Args:
        'uri': (str) uri to download
    Returns:
        None if nothing can be resolved, otherwise:
        If uri resolves to a channel or a claim in a channel:
            'certificate': {
                'address': (str) claim address,
                'amount': (float) claim amount,
                'effective_amount': (float) claim amount including supports,
                'claim_id': (str) claim id,
                'claim_sequence': (int) claim sequence number,
                'decoded_claim': (bool) whether or not the claim value was decoded,
                'height': (int) claim height,
                'depth': (int) claim depth,
                'has_signature': (bool) included if decoded_claim
                'name': (str) claim name,
                'supports: (list) list of supports [{'txid': txid,
                                                     'nout': nout,
                                                     'amount': amount}],
                'txid': (str) claim txid,
                'nout': (str) claim nout,
                'signature_is_valid': (bool), included if has_signature,
                'value': ClaimDict if decoded, otherwise hex string
            }
        If uri resolves to a channel:
            'claims_in_channel': [
                {
                    'address': (str) claim address,
                    'amount': (float) claim amount,
                    'effective_amount': (float) claim amount including supports,
                    'claim_id': (str) claim id,
                    'claim_sequence': (int) claim sequence number,
                    'decoded_claim': (bool) whether or not the claim value was decoded,
                    'height': (int) claim height,
                    'depth': (int) claim depth,
                    'has_signature': (bool) included if decoded_claim
                    'name': (str) claim name,
                    'supports: (list) list of supports [{'txid': txid,
                                                         'nout': nout,
                                                         'amount': amount}],
                    'txid': (str) claim txid,
                    'nout': (str) claim nout,
                    'signature_is_valid': (bool), included if has_signature,
                    'value': ClaimDict if decoded, otherwise hex string
                }
            ]
        If uri resolves to a claim:
            'claim': {
                'address': (str) claim address,
                'amount': (float) claim amount,
                'effective_amount': (float) claim amount including supports,
                'claim_id': (str) claim id,
                'claim_sequence': (int) claim sequence number,
                'decoded_claim': (bool) whether or not the claim value was decoded,
                'height': (int) claim height,
                'depth': (int) claim depth,
                'has_signature': (bool) included if decoded_claim
                'name': (str) claim name,
                'channel_name': (str) channel name if claim is in a channel
                'supports: (list) list of supports [{'txid': txid,
                                                     'nout': nout,
                                                     'amount': amount}]
                'txid': (str) claim txid,
                'nout': (str) claim nout,
                'signature_is_valid': (bool), included if has_signature,
                'value': ClaimDict if decoded, otherwise hex string
            }
        }
    """
    res = _request('resolve', uri=uri)
    return res

def resolve_name(name):
    """Resolve stream info from a LBRY name

    Args:
        'name': (str) name to look up, do not include lbry:// prefix
    Returns:
        (dict) Metadata dictionary from name claim, None if the name is not
                resolvable
    """
    res = _request('resolve_name', name=name)
    return res

def send_amount_to_address(amount, address):
    """Send credits to an address

    Args:
        'amount': (float) the amount to send
        'address': (str) the address of the recipient in base58
    Returns:
        (bool) true if payment successfully scheduled
    """
    res = _request('send_amount_to_address', amount=amount, address=address)
    return res

def settings_get():
    """Get daemon settings

    Returns:
        (dict) Dictionary of daemon settings
        See ADJUSTABLE_SETTINGS in lbrynet/conf.py for full list of settings
    """
    res = _request('settings_get')
    return res

def settings_set(**kwargs):
    """Set daemon settings

    Args:
        'run_on_startup': (bool) currently not supported
        'data_rate': (float) data rate,
        'max_key_fee': (float) maximum key fee,
        'disable_max_key_fee': (bool) true to disable max_key_fee check,
        'download_directory': (str) path of where files are downloaded,
        'peer_port': (int) port through which daemon should connect,
        'max_upload': (float), currently not supported
        'max_download': (float), currently not supported
        'download_timeout': (int) download timeout in seconds
        'search_timeout': (float) search timeout in seconds
        'cache_time': (int) cache timeout in seconds
    Returns:
        (dict) Updated dictionary of daemon settings
    """
    res = _request('settings_set', **kwargs)
    return res

def status(session_status=False):
    """Return daemon status

    Args:
        'session_status' (optional): (bool) true to return session status,
            default is false
    Returns:
        (dict) Daemon status dictionary
    """
    res = _request('status', session_status=session_status)
    return res


def stream_cost_estimate(name, size=None):
    """Get estimated cost for a lbry stream

    Args:
        'name': (str) lbry name
        'size' (optional): (int) stream size, in bytes. if provided an sd blob
                            won't be downloaded.
    Returns:
        (float) Estimated cost in lbry credits, returns None if uri is not
            resolveable
    """
    res = _request('stream_cost_estimate', name=name, size=size)
    return res

def transaction_list():
    """List transactions belonging to wallet

    Args:
        None
    Returns:
        (list) List of transactions
    """
    res = _request('transaction_list')
    return res

def transaction_show(txid):
    """Get a decoded transaction from a txid

    Args:
        'txid': (str) txid of transaction
    Returns:
        (dict) JSON formatted transaction
    """
    res = _request('transaction_show', txid=txid)
    return res

def wallet_balance(address=None, include_uncomfirmed=None):
    """Return the balance of the wallet

    Args:
        'address' (optional): If address is provided only that balance will be given
        'include_unconfirmed' (optional): If set unconfirmed balance will be included in
         the only takes effect when address is also provided.

    Returns:
        (float) amount of lbry credits in wallet
    """
    res = _request('wallet_balance', address=address, include_uncomfirmed=include_uncomfirmed)
    return res

def wallet_is_address_mine(address):
    """Checks if an address is associated with the current wallet.

    Args:
        'address': (str) address to check in base58
    Returns:
        (bool) true, if address is associated with current wallet
    """
    res = _request('wallet_is_address_mine', address=address)
    return res

def wallet_list():
    """List wallet addresses

    Returns:
        List of wallet addresses
    """
    res = _request('wallet_list')
    return res

def wallet_new_address():
    """Generate a new wallet address

    Returns:
        (str) New wallet address in base58
    """
    res = _request('wallet_new_address')
    return res

def wallet_public_key(address):
    """Get public key from wallet address

    Args:
        'address': (str) wallet address in base58
    Returns:
        (list) list of public keys associated with address.
            Could contain more than one public key if multisig.
    """
    res = _request('wallet_public_key', address=address)
    return res

def wallet_unused_address():
    """Return an address containing no balance, will create a new address if there is none.

    Returns:
        (str) Unused wallet address in base58
    """
    res = _request('wallet_unused_address')
    return res

