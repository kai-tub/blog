const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  // testing jit mode
  mode: 'jit',
  purge: {
    content: [
      "*.tmpl",
      "./shortcodes/**/*.tmpl",
      "./templates/**/*.tmpl",
    ],
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    screens: {
      // small-m from chrome
      'ssm': '375px',
      ...defaultTheme.screens,
    },
    extend: {
      maxWidth: {
        '1/10': '10%',
        '1/5': '20%',
        '1/4': '25%',
        '1/2': '50%',
        '3/4': '75%',
      },
      minHeight: {
        'screen-1/4': '20vh',
        'screen-1/3': '33vh',
        'screen-1/2': '50vh',
      },
      backgroundImage: theme => ({
        'hero-pattern': "url('/assets/images/hero-pattern.jpg')",
      }),
      // typography: theme => ({
      //   DEFAULT: {
      //     css: {

      //     }
      //   }
      // })
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/typography'),
    require('daisyui'),
    // needs to come after typography!
  ],
  daisyui: {
    themes: [
      "halloween",
      // "light",
      {
        'light': {
          'primary': '#570df8',
          'primary-focus': '#4506cb',
          'primary-content': '#ffffff',
          'secondary': '#f000b8',
          'secondary-focus': '#bd0091',
          'secondary-content': '#ffffff',
          'accent': '#37cdbe',
          'accent-focus': '#2aa79b',
          'accent-content': '#ffffff',
          'neutral': '#3d4451',
          'neutral-focus': '#2a2e37',
          'neutral-content': '#ffffff',
          'base-100': '#e8e8e8',
          'base-200': '#c2c2c2',
          'base-300': '#7a7a7a',
          'base-content': '#1f2937',
          'info': '#2094f3',
          'success': '#009485',
          'warning': '#ff9900',
          'error': '#ff5724',
        },
      }
    ]
  }
}
