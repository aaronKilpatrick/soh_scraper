from BcScraper import BcScraper

def add_path(path: str)->None:
    '''Adds path to paths.txt'''
    print('Add Paths')
    try:
        f = open('C:\paths.txt', 'a')

        f.write(path)

        f.close()
    except:
        print('Could not add path')
    
    print('Path added')

def remove_path()->None:
    ''''''
    paths = get_paths()
    print('Remove Path')
    for i, path in enumerate(paths):
        print(f'{i} - {path}', end='')
    print('\n\nType number of path.')
    
    try:
        pathNum = input('Path to remove: ')
        if pathNum is not 'quit':
            pathNum = int(pathNum)            
            del paths[pathNum]
    except:
        print('Invalid selection')

    try:
        f = open('C:\paths.txt', 'w')
        f.writelines(paths)
        f.close()
    except:
        print('Could not delete path')

def get_paths()->list:
    '''gets paths file'''
    # Open file and push to list
    try:
        f = open('C:\paths.txt', 'r')
        paths = f.readlines()
        f.close()
        return paths
    except:
        print('Could not find paths.txt.\nUse \'add paths\' to add first path.')
    
    

def get_help():
    '''Prints help docs to console'''
    print("\nBikeCorp Web Scraper Help\n")
    print('Command - quit\n\texits program\n\n')
    
    print('Command - scrape')
    print('\tScrapes bikecorp website for stock and SKUs, converts to')
    print('\tcsv that will save to desktop\n')

    print('Command - add path')
    print('\tPrompts for new path of product page')
    print('\tAppends path to file')
    print('\tPlease only add filepath between { } in example:')
    print('\thttps://www.bikecorp.com.au/{clothing/jerseys-sx0511}')
    print('\tSaves CSV to desktop\n')
    print('\tType \'quit\' to go to main menu\n')

    print('Command - rem path')
    print('\tPrints list of paths saved in system')
    print('\tEnter corresponding number into promt to delete that item')
    print('\tType \'quit\' to go to main menu')

print("\nWelcome to BikeCorp Stock Scraper")
print("Type 'help' to get help.\n")

while True:
    com = input("\n>> ")

    if com == 'quit':
        print("Goodbye")
        exit()

    elif com == 'help':
        get_help()
    
    elif com == 'add path':
        paths = input('Add url path: ')
        if paths == 'quit':
            continue
        add_path(f'\n{paths}')

    elif com == 'rem path':
        remove_path()

    elif com == 'scrape':
        bc = BcScraper()

        paths = get_paths()
        for path in paths:
            bc.scrape_stock_from_category(path)
        bc.write_to_csv()
    
    else:
        print('Invalid input')
