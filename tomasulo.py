from Architecture import *
import Config as cfg

if __name__ == '__main__':
    tomasulo = Architecture()
    results = tomasulo.start()
    cfg.results = results
