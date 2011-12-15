def main(args):
    import pickle
    import os
    os.popen('touch ~/Documents/dump.txt')
    f = open('~/Documents/dump.txt','wb')
    pickle.dumps(args,f)
    f.close()

if __name__ == '__main__':
    main(args)
