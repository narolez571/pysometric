import pygame
from pygame.locals import *

from isometric import settings
from isometric.lib.perlin.perlin import PerlinNoiseFactory


class TileTable(object):
    def __init__(self, tilefile):
        self.tilefile = tilefile
        self.tiledict_coords = {}
        self.tiledict = {}

        self.tile_width = settings.TILEWIDTH
        self.tile_height = settings.TILEHEIGHT

        self._load_tile_table()

    def _load_tile_table(self):
        image = pygame.image.load(self.tilefile).convert_alpha()
        image_width, image_height = image.get_size()
        
        for i, x in enumerate(['GRASS_NONE_1', 'GRASS_NONE_2', 'GRASS_MUD_1', 'GRASS_MUD_2']):
            self.tiledict_coords[x] = (i, 0)
        for i, x in enumerate(['OCEAN_BANK_34', 'OCEAN_BANK_4', 'OCEAN_BANK_3', 
                               'OCEAN_BANK_14', 'OCEAN_NONE_1', 'OCEAN_NONE_2', 
                               'OCEAN_BANK_23', 'OCEAN_BANK_1', 'OCEAN_BANK_2', 
                               'OCEAN_BANK_12']):
            self.tiledict_coords[x] = (i, 8)

        self.tiledict_coords['OCEAN_BANK_34'] = (0, 8)

        self.tiledict_coords['OCEAN_BANK_123'] = (4,10)
        self.tiledict_coords['OCEAN_BANK_234'] = (5,10)
        self.tiledict_coords['OCEAN_BANK_134'] = (6,10)
        self.tiledict_coords['OCEAN_BANK_124'] = (3,10)

        self.tiledict_coords['OCEAN_BANK_13'] = (2, 9)
        self.tiledict_coords['OCEAN_BANK_24'] = (1, 9)
        self.tiledict_coords['OCEAN_BANK_1234'] = (1, 10)
        

        for k,v in self.tiledict_coords.items():
            self.tiledict[k] = image.subsurface( (self.tile_width * v[0], 
                                                  self.tile_height * v[1],
                                                  self.tile_width, 
                                                  self.tile_height) )


class MapCell(object):
    def __init__(self, tile_key):
        self.tile_key = tile_key

class MapRow(object):
    def __init__(self):
        self.row = []

class TileMap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cols = []

        self.tile_width = settings.TILEWIDTH
        self.tile_height = settings.TILEHEIGHT

        self._createMap()

    def _createMap(self):
        size = settings.PNF_MAP_SIZE

        pnf = PerlinNoiseFactory(size, settings.PNF_TILEDIM, settings.PNF_REPEATS)
        pnm = pnf._generate_map()

        for j in xrange(0, self.height):
            m = MapRow()
            for i in xrange(0, self.width):
                mc = MapCell(pnm.tilekey_map[i][j])
                m.row.append(mc)
            self.cols.append(m)

    def drawMap(self, camera_offset, screen, tiledict):
        # Overlay grass tiles first
        for j in xrange(0, self.height):
            for i in xrange(0, self.width):
                screen.blit(tiledict['GRASS_NONE_1'], 
                            (i*64 + (j%2 * 32) + camera_offset[0], j*16 + camera_offset[1]))

        # Then create all ocean/bank tiles
        for j in xrange(0, self.height):
            for i in xrange(0, self.width):
                screen.blit(tiledict[ self.cols[j].row[i].tile_key ], 
                            (i*64 + (j%2 * 32) + camera_offset[0], j*16 + camera_offset[1]))



    def printMap(self):
        for j in xrange(0, self.height):
            sys.stdout.write("[ ")
            for i in xrange(0, self.width):
                sys.stdout.write("%s " % self.cols[j].row[i].tile_key)
            print "]"
        print "\n"

