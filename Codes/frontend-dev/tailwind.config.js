module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      height: {
        128: '29rem',
      },
    },
  },
  plugins: [require('daisyui')],
  daisyui: {
    styled: true,
    utils: true,
    logs: false,
    themes: false,
    base: false,
  },
};
