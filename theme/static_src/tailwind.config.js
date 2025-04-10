/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /* Templates within theme app */
        '../templates/**/*.html',

        /* Main templates directory of the project */
        '../../templates/**/*.html',

        /* Templates in other django apps */
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            keyframes: {
                'jello-vertical': {
                    '0%': { transform: 'scale3d(1, 1, 1)' },
                    '30%': { transform: 'scale3d(0.75, 1.25, 1)' },
                    '40%': { transform: 'scale3d(1.25, 0.75, 1)' },
                    '50%': { transform: 'scale3d(0.85, 1.15, 1)' },
                    '65%': { transform: 'scale3d(1.05, 0.95, 1)' },
                    '75%': { transform: 'scale3d(0.95, 1.05, 1)' },
                    '100%': { transform: 'scale3d(1, 1, 1)' },
                },
            },
            animation: {
                'jello-vertical': 'jello-vertical 0.9s both',
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
};