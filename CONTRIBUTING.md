# Contributing to ShopAssist RAG

Thank you for your interest in contributing to ShopAssist RAG!

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists
2. Create a new issue with:
   - Clear description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information (OS, Python version)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
```bash
   git checkout -b feature/your-feature-name
```

3. **Make your changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation

4. **Test your changes**
```bash
   python tests/test_queries.py
```

5. **Commit with clear messages**
```bash
   git commit -m "Add feature: description"
```

6. **Push to your fork**
```bash
   git push origin feature/your-feature-name
```

7. **Create a Pull Request**
   - Describe your changes
   - Reference related issues
   - Include test results

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions focused and small

### Documentation
- Update README.md for user-facing changes
- Update docs/ for architecture changes
- Add inline comments for complex logic
- Include examples for new features

### Testing
- Add tests for new features
- Ensure existing tests pass
- Test with different query types
- Validate on sample data

## Areas for Contribution

### High Priority
- [ ] Add authentication to API
- [ ] Implement rate limiting
- [ ] Add more evaluation metrics
- [ ] Improve error handling
- [ ] Optimize vector search

### Medium Priority
- [ ] Add more data sources
- [ ] Implement query suggestions
- [ ] Add conversation history
- [ ] Create Docker deployment
- [ ] Add Prometheus metrics

### Nice to Have
- [ ] Multi-language support
- [ ] Voice interface
- [ ] Advanced analytics dashboard
- [ ] A/B testing framework
- [ ] Custom model fine-tuning

## Questions?

Feel free to open an issue for questions or discussion!