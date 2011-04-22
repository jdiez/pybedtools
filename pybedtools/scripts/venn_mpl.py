#/usr/bin/python

import optparse
import sys
import os
import pybedtools



def venn_mpl(a, b, c, colors=None, outfn=None, labels=None):

    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle
    except ImportError:
        sys.stderr.write('matplotlib is required to make a Venn diagram with %s\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)

    a = pybedtools.BedTool(a)
    b = pybedtools.BedTool(b)
    c = pybedtools.BedTool(c)

    if colors is None:
        colors = ['r','b','g']

    radius = 6.0
    center = 0.0
    offset = radius / 2

    if labels is None:
        labels = ['a','b','c']

    circle_a = Circle(xy = (center-offset, center+offset), radius=radius, edgecolor=colors[0], label=labels[0])
    circle_b = Circle(xy = (center+offset, center+offset), radius=radius, edgecolor=colors[1], label=labels[1])
    circle_c = Circle(xy = (center,        center-offset), radius=radius, edgecolor=colors[2], label=labels[2])


    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111)

    for circle in (circle_a, circle_b, circle_c):
        circle.set_facecolor('none')
        circle.set_linewidth(3)
        ax.add_patch(circle)

    ax.axis('tight')
    ax.axis('equal')
    ax.set_axis_off()


    kwargs = dict(horizontalalignment='center')

    # Unique to A
    ax.text( center-2*offset, center+offset, str((a - b - c).count()), **kwargs)

    # Unique to B
    ax.text( center+2*offset, center+offset, str((b - a - c).count()), **kwargs)

    # Unique to C
    ax.text( center, center-2*offset, str((c - a - b).count()), **kwargs)

    # A and B not C
    ax.text( center, center+2*offset-0.5*offset, str((a + b - c).count()), **kwargs)

    # A and C not B
    ax.text( center-1.2*offset, center-0.5*offset, str((a + c - b).count()), **kwargs)

    # B and C not A
    ax.text( center+1.2*offset, center-0.5*offset, str((b + c - a).count()), **kwargs)

    # all
    ax.text( center, center, str((a + b + c).count()), **kwargs)

    ax.legend(loc='best')

    fig.savefig(outfn)

    plt.close(fig)

if __name__ == "__main__":

    usage = """
    Given 3 files, creates a 3-way Venn diagram of intersections using matplotlib.  
    
    Numbers are placed on the diagram.  If you don't have matplotlib installed.
    try venn_gchart.py to use the Google Chart API instead.

    The values in the diagram assume:

        * unstranded intersections
        * no features that are nested inside larger features
    """
    op = optparse.OptionParser()
    op.add_option('-a', help='File to use for the left-most circle')
    op.add_option('-b', help='File to use for the right-most circle')
    op.add_option('-c', help='File to use for the bottom circle')
    op.add_option('--labels',
                  help='Optional comma-separated list of '
                       'labels for a, b, and c')
    op.add_option('--colors', default='r,b,g',
                  help='Comma-separated list of matplotlib-valid colors '
                       'for circles a, b, and c.  E.g., --colors=r,b,k')
    op.add_option('-o', default='out.png', 
                  help='Output file to save as.  Extension is '
                       'meaningful, e.g., out.pdf, out.png, out.svg.  Default is "%default"')
    op.add_option('--test', action='store_true', help='run test, overriding all other options.')
    options,args = op.parse_args()

    reqd_args = ['a','b','c']
    if not options.test:
        for ra in reqd_args:
            if not getattr(options,ra):
                sys.stderr.write('Missing required arg "%s"\n' % ra)
                sys.exit(1)

    if options.test:
        pybedtools.bedtool.random.seed(1)
        a = pybedtools.example_bedtool('rmsk.hg18.chr21.small.bed')
        b = a.random_subset(100).shuffle(genome='hg19')
        b = b.cat(a.random_subset(100))
        c = a.random_subset(200).shuffle(genome='hg19')
        c = c.cat(b.random_subset(100))
        options.a = a.fn
        options.b = b.fn
        options.c = c.fn
        options.colors='r,b,g'
        options.o = 'out.png'
        options.labels = 'a,b,c'

    venn_mpl(a=options.a, b=options.b, c=options.c, 
             colors=options.colors.split(','),
             labels=options.labels.split(','), 
             outfn=options.o)

def main():
    """
    plot a venn chart of 3 bed files with matplotlib
    """
    venn_mpl()