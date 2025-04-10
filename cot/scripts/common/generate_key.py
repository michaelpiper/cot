from Crypto.Random import get_random_bytes
import base64
import argparse
import sys

def generate_aes_key(key_size=32):
    """
    Generate a secure AES key (128/192/256-bit)
    :param key_size: 16 (128-bit), 24 (192-bit), or 32 (256-bit)
    :return: Base64-encoded key
    """
    valid_sizes = {16, 24, 32}
    if key_size not in valid_sizes:
        raise ValueError(f"Key size must be 16, 24, or 32 bytes, got {key_size}")
    
    # Generate cryptographically secure random bytes
    key = get_random_bytes(key_size)
    
    # Return URL-safe base64 encoded string
    return base64.urlsafe_b64encode(key).decode('utf-8')

def main():
    parser = argparse.ArgumentParser(description='Generate secure encryption keys for banking applications')
    parser.add_argument('--size', type=int, choices=[16, 24, 32], default=32,
                       help='Key size in bytes (16=128-bit, 24=192-bit, 32=256-bit)')
    parser.add_argument('--env', action='store_true', 
                       help='Output as environment variable format')
    
    args = parser.parse_args()
    
    try:
        key = generate_aes_key(args.size)
        if args.env:
            print(f"BANKING_ENC_KEY={key}")
        else:
            print(f"Generated AES-{args.size*8}-bit key:\n{key}")
    except Exception as e:
        print(f"Error generating key: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()