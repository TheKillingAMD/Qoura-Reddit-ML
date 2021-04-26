import hash from 'string-hash';
import color from 'tinycolor2';

export default function Avatar({ text }) {
    console.log(text);
    const name = text
        .split(' ')
        .map(w => w[0].toUpperCase())
        .reduce((acc, cur) => acc + cur, '')
        .slice(0, 2);
    text = text.replace(/\s+/, '');
    const hashed = hash(text);
    console.log('H:', hashed);
    const c = color({ h: hashed % 360, s: 0.95, l: 0.5 });
    const c1 = c.toHexString();
    const c2 = c.triad()[1].toHexString();
    console.log(c1, c2);
    return (
        <svg role='img' aria-label={text} width='40' height='40' viewBox='0 0 80 80'>
            <defs>
                <linearGradient x1='0%' y1='0%' x2='100%' y2='100%' id={text}>
                    <stop stopColor={c1} offset='0%' />
                    <stop stopColor={c2} offset='100%' />
                </linearGradient>
            </defs>
            <g stroke='none' strokeWidth='1' fill='none'>
                <circle fill={`url(#${text})`} cx='40px' cy='40px' r='40px' />
                <text
                    x='50%'
                    y='50%'
                    fill='white'
                    fontSize='30'
                    textAnchor='middle'
                    dy='.3em'
                    fontWeight='600'
                >
                    {name}
                </text>
            </g>
        </svg>
    );
}
