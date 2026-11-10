# Contributing

Thanks for considering a contribution.

## Development setup

Follow the backend and frontend setup instructions in the root README.

## Quality expectations

- Keep metric calculations in the backend service layer.
- Add tests for new calculations, validation rules and edge cases.
- Do not silently discard rows or make causal claims from slice comparisons.
- Keep API error messages actionable and avoid exposing secrets.
- Update relevant documentation when behavior changes.

## Suggested workflow

1. Create a focused branch.
2. Make a small, meaningful change.
3. Run backend tests and frontend production build.
4. Update docs and sample data if needed.
5. Open a pull request with the motivation, implementation notes and test evidence.
