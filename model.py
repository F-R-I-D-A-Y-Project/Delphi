import argparse

def get_user_input() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Download stock data from Alpha Vantage.')
    parser.add_argument('-t', '--train', type=str, help='Symbol to train the model and model version', nargs=2)
    parser.add_argument('-e', '--eval', type=str, help='Company symbol to be evalueated and model version', nargs=2)
    
    return parser.parse_args()

def train_model_v0(symbol: str) -> None: ...

def train_model_v1(symbol: str) -> None: ...

def train_model_v2(symbol: str) -> None: ...

def eval_model_v0(symbol: str) -> None: ...

def eval_model_v1(symbol: str) -> None: ...

def eval_model_v2(symbol: str) -> None: ...

def train_model(symbol: str, model_version: str) -> None:
    symbol = symbol.upper()
    print(f'Training model for {symbol} with version {model_version}')
    match model_version:
        case 'v0': train_model_v0(symbol)
        case 'v1': train_model_v1(symbol)
        case 'v2': train_model_v2(symbol)
        case _: raise ValueError('Model version must be v0, v1 or v2')


def main():
    args = get_user_input()
    if args.train:
        if args.train[1] not in ['v0', 'v1', 'v2']:
            raise ValueError('Model version must be v0, v1 or v2')
        train_model(*args.train)


if __name__ == '__main__':
    main()