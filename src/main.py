from scraper import UserScraper

def main():
    '''
    will = UserScraper('https://www.mountainproject.com/user/200305518/william-jiang')
    print(will.get_dict())

    '''
    cam = UserScraper('https://www.mountainproject.com/user/200580738/cameron-nachreiner')
    print(cam.get_dict())
    

if __name__ == "__main__":
    main()
