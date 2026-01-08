import container from 'markdown-it-container';
import attrs from 'markdown-it-attrs';
import ins from 'markdown-it-ins';
import mark from 'markdown-it-mark';
import prism from 'markdown-it-prism';
import kroki from '@kazumatu981/markdown-it-kroki'

/**
 * @type {import('@marp-team/marp-cli').Config<typeof import('@marp-team/marpit').Marpit>["engine"]}
 */
export default ({ marp }) => marp
  .use(kroki,{
    entrypoint: "https://kroki.io",
  })
  .use(prism)
  .use(mark)
  .use(ins)
  .use(attrs)
  .use(container, '_')
  .use(container, 'c');
