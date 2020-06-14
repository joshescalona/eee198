import imgkit

ctr = 0
fn = ''

outname = ''
while ctr < 1:

    # fn = fn.replace(fn, 'templates/map' + str(ctr) + '.html')
    fn = 'templates/map0.html'
    outname = outname.replace(outname, 'map_images/image' + str(ctr) + '.jpg')

    options={'xvfb': ''}
    # imgkit.from_url('http://google.com', 'out.jpg', options=options)
    imgkit.from_file(fn, outname, options=options)
    ctr += 1
