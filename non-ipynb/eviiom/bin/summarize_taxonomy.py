import sys
import biom

t = biom.load_table(sys.argv[1])
l = int(sys.argv[2])

f = lambda i, m: "Other" if m['taxonomy'] is None else m['taxonomy'][l]
collapsed = t.collapse(f, axis='observation', norm=False)
f = open(sys.argv[1] + '.L%d.txt' % l, 'w')
f.write(collapsed.to_tsv())
f.close()
