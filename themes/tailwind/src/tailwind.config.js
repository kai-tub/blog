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
      "light",
    ]
  }
}
