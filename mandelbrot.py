#!/usr/bin/env python 

# Generate numbers from the mandelbrot set

import numpy as np
from PIL import Image

# Find whether a complex number c is in the mandelbrot set, by iterating up to
# 'maxi' times over the test function
# return the number of iterations it took to determine whether the item was in the set
# if the number of iterations is maxi then the number is in the set 
def m_member(creal, cimag, maxi=100): 
    zreal = creal
    zimag = cimag
    # iterating from z=(0+0j) but first value of z**2+c will then be 'c' so start there 
    for i in range(maxi):
        zrealsq = zreal*zreal # multiplication faster than power function
        zimagsq = zimag*zimag
        if zrealsq + zimagsq > 4.0: # manually calc the abs value as it's faster than sqrt
            return i
        # now calculate the next value of z**2+c
        zimag = 2* zreal*zimag + cimag
        zreal = zrealsq - zimagsq + creal       
    return maxi


# create and return a new image from the array passed
# scale the pixel values based on the range of values found in the array
def m_image(m_array):
    maxval = m_array.max()
    pixscale = int(255/(maxval - m_array.min()))
    width, height = m_array.shape
    img = Image.new("RGB",(width,height))
    c1 = maxval / 3
    c2 = c1 * 2
    c3 = maxval
    
    for x in range(width):
        for y in range(height):
            v = m_array[x,y]
            pv=int(256-m_array[x,y]*pixscale)
            
            if v == maxval: # i.e. the point is inside the set
                pixval = (0,0,0) # make it black
            elif v < c1: # mainly blue
                pixval = (0,50,pv)
            elif v < c2: # mainly green
                pixval=(0,pv,50)
            else: # must be in the red
                pixval=(pv,0,0)
            img.putpixel((x,y), pixval)
    return img

# find the zero in a range and scale to the argument 'w'
def find_zero(xmin,xmax,w):
    rng = xmax - xmin
    if rng <= 0:
        return -2 # range error
    elif xmin <= 0.0 and xmax >= 0.0:
        return int(w*abs(xmin)/rng)
    else:
        return -1 # no zero in the span provided


# generate axes on the image
def m_axes(xmin,xmax,ymin,ymax, img, w,h):
    dxval = find_zero(xmin, xmax, w)
    yval = find_zero(ymin, ymax, h)
    pv=(255,255,255) # white
    if yval > 0 :
        for x in range(w):
            img.putpixel((x,yval), pv)
    if xval > 0:
        for y in range(h):
            img.putpixel((xval,y), pv)

# generate labels 
def m_label(xmin,xmax,ymin,ymax, img):
    txt = str(xmin)+','+str(xmax)+','+str(ymin)+','+str(ymax)
    d = ImageDraw.Draw(img)
    xval = find_zero(xmin, xmax, w)
    yval = find_zero(ymin, ymax, h)
    pv=(255,0,0) # red
    
    if yval > 0 :
        for x in range(w):
            img.putpixel((x,yval), pv)
    if xval > 0:
        for y in range(h):
            img.putpixel((xval,y), pv)

# generate mandelbrot set in the range with the resolution specified
def m_generate(xmin,xmax,ymin,ymax,width,height,maxi):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    m_array = np.empty((width,height))
    for i in range(width):
        for j in range(height):
            m_array[i,j] = m_member(r1[i],r2[j],maxi)
    
    return m_array


# generate mandelbrot set and output it as a color image ifile
def mandelbrot(xmin=-2.0, xmax=0.5, ymin=-1.25,ymax=1.25,
               width=500, height=500, maxi=50, ifile='mandelpic.bmp',
               draw_axes = False):
    # generate an array of values which are the num of iterations it took
    # to determine if the number was in or out of the set
    m_array = m_generate(xmin,xmax,ymin,ymax,width,height,maxi)

    #generate an image using the array we just 
    img=m_image(m_array)

    # add axes to the picture if required
    if draw_axes:
        m_axes(xmin, xmax,ymin,ymax, img, width, height)

    # save the image file
    img.save(ifile)

