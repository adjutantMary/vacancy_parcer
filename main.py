from src.utils import get_save_data, get_search, make_top_n

if __name__ == "__main__":
    get_save_data(make_top_n(get_search()))
