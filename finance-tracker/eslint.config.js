import antfu from '@antfu/eslint-config';

export default antfu({
  rules: {
    'indent': ['error', 2],
    'style/semi': ['error', 'always'],
    'antfu/if-newline': 'off',
    'antfu/consistent-list-newline': 'off',
    'no-unused-vars': 'warn',
    'vue/custom-event-name-casing': ['error', 'kebab-case'],
    'antfu/top-level-function': 'off',
    'no-restricted-imports': ['error', { patterns: ['**/composables/UI/*', '../UI/*', './UI/*'] },
    ],
  },

  ignores: ['node_modules', '*.d.ts', '.nuxt', '.output', '.gitlab-ci.yml', 'Dockerfile', '*.d.ts', '**/*.d.ts'],
});
