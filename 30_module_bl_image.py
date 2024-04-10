def linear_to_sRGB(linear_value):
    if linear_value <= 0.0031308:
        sRGB_value = 12.92 * linear_value
    else:
        sRGB_value = 1.055 * (linear_value ** (1/2.4)) - 0.055
    return sRGB_value

def math_UVPosition_By_Tile(xt, yt, tile_count_x, tile_count_y):
    
    """  !METHOD!
    Divides the UV into Tiles based on Tilecount and gets the Center Position of that Square

    Keyword arguments:
    :param int xt,yt:                       Squareposition
    :param: int tile_count_x,tile_count_y:  Amount of Squares per Axies
    :return: float uv_x, uv_y:              Postion on UV 0.0-1.0
    """

    
    uv_x = (xt / tile_count_x) + (0.5 / tile_count_x)
    uv_y = (yt / tile_count_y) + (0.5 / tile_count_y)
    
    #Add Debug Here?

    return uv_x, uv_y

def math_PixelIndex_By_TileNumber(xt, yt, width, height, tile_count_x, tile_count_y, uv_offset_x=0, uv_offset_y=0):
    """ !METHOD! 
    Uses the Sizes of the Texture, the Tilecount and Calculates the Index of the Pixel in the Array

    Keyword arguments:
    :param int xt,yt:                       Squareposition
    :param float width,height:              Size of Image
    :param: int tile_count_x,tile_count_y:  Amount of Squares per Axies
    :return: int index:                     index of Pixel inside a Array
    """
        
    mid_x = (xt * width // tile_count_x) + (width // tile_count_x // 2) + int(uv_offset_x)
    mid_y = (yt * height // tile_count_y) + (height // tile_count_y // 2) + int(uv_offset_y)
    index = (mid_y * width + mid_x) * 4

    functionname="CalculateMiddlePixel"

    printLog(src=functionname, msg="xt: " + str(xt) + " yt: " + str(yt) + " width: " + str(width) + " height: " + str(height) + " tile_count_x: " + str(tile_count_x) + " tile_count_y: " + str(tile_count_y) + " uv_offset_x: " + str(uv_offset_x) + " uv_offset_y: " + str(uv_offset_y), subtype=LOGTYPE.IN)
    printLog(src=functionname, msg="index: " + str(index), subtype=LOGTYPE.OUT)
     
    return index 
    
def math_getTileFromUVXY(tilecountx, tilecounty, x,y):    
    
    """ !METHOD!
    Calculates the Basetile from the Tilecount and the UV Coordinate

    Keyword arguments:
    xxx                       N/A #
    """


    segment_x = int(min(math.floor(x * tilecountx), tilecountx - 1))
    segment_y = int(min(math.floor(y * tilecounty), tilecounty - 1))
    #printLog(src="calculateSegment", subtype=LOGTYPE.INFO, msg="Segmentcoordinates"+str(segment_x)+"/"+str(segment_y)) 
    
    return segment_x,segment_y  
   
def math_getTileFromUV(tilecountx, tilecounty, uv):
    """ !METHOD!
    Calculates the Basetile from the Tilecount and the UV Coordinate

    Keyword arguments:
    xxx                       N/A #
    """



    segment_x = int(min(math.floor(uv.x * tilecountx), tilecountx - 1))
    segment_y = int(min(math.floor(uv.y * tilecounty), tilecounty - 1))
    #printLog(src="calculateSegment", subtype=LOGTYPE.INFO, msg="Segmentcoordinates"+str(segment_x)+"/"+str(segment_y)) 
    
    return segment_x,segment_y  

def img_readPixel_By_Index(img, index):
    """ !METHOD!
    Gets the Color of a Pixel inside a Pixel Array of an Image

    Keyword arguments:
    :param Image img:                       Image to get the Pixel From
    :return: int[4] index:                  4 Pixels representing RGBA
    """
    return img.pixels[index:index + 4]

def readImagePixel(image, x, y):
    """ !METHOD!
    Reads the Pixel Data of an Image

    Keyword arguments:
    :param Image img:                       Image to get the Pixel From
    :return: int[4] index:                  4 Pixels representing RGBA
    """
    
    width = image.size[0]
    height = image.size[1]
    
    index = img_getImagePixelIndex(x, y, width)
    pixels=image.pixels[index:index + 4]
    
    return pixels

def img_getImagePixelIndex(xt, yt, imagewidth):
    """ !METHOD!
    Gets the Color of a Pixel inside a Pixel Array of an Image

    Keyword arguments:
    :param Image img:                       Image to get the Pixel From
    :return: int[4] index:                  4 Pixels representing RGBA
    """
    
    return (yt * imagewidth + xt)*4

def img_getTilesetPixelIndex(xt, yt, tilesizex):
    """ !METHOD!
    Gets the Color of a Pixel inside a Pixel Array of an Image

    Keyword arguments:
    :param Image img:                       Image to get the Pixel From
    :return: int[4] index:                  4 Pixels representing RGBA
    """
    
    return yt * (tilesizex) + xt 

def math_getIndexByTile(xt, yt, tile_count_x):
    
    return yt * tile_count_x + xt