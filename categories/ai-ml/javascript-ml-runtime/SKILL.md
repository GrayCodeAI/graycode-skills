---
name: javascript-ml-runtime
description: "Runs state-of-the-art machine learning models directly in JavaScript/TypeScript in browsers and server runtimes, covering NLP, computer vision, audio, and multimodal tasks with WebGPU/WASM."
license: Apache-2.0
tags:
- machine-learning
- javascript
- typescript
- transformers
- webgpu
---

# Transformers.js - Machine Learning for JavaScript

Transformers.js enables running state-of-the-art machine learning models directly in JavaScript across browsers and server-side runtimes (Node.js, Bun, Deno), with no Python server required.

## When to Use This Skill

Use this skill when you need to:
- Run ML models for text analysis, generation, or translation in JavaScript
- Perform image classification, object detection, or segmentation
- Implement speech recognition or audio processing
- Build multimodal AI applications (text-to-image, image-to-text, etc.)
- Run models client-side in the browser without a backend

## Installation

### NPM Installation
```bash
npm install @huggingface/transformers
```

### Browser Usage (CDN)
```javascript
<script type="module">
  import { pipeline } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers';
</script>
```

## Core Concepts

### 1. Pipeline API
The pipeline API is the easiest way to use models. It groups together preprocessing, model inference, and postprocessing:

```javascript
import { pipeline } from '@huggingface/transformers';

// Create a pipeline for a specific task
const pipe = await pipeline('sentiment-analysis');

// Use the pipeline
const result = await pipe('I love transformers!');
// Output: [{ label: 'POSITIVE', score: 0.999817686 }]

// IMPORTANT: Always dispose when done to free memory
await pipe.dispose();
```

**⚠️ Memory Management:** All pipelines must be disposed with `pipe.dispose()` when finished to prevent memory leaks. See examples in Code Examples for cleanup patterns across different environments.

### 2. Model Selection
You can specify a custom model as the second argument:

```javascript
const pipe = await pipeline(
  'sentiment-analysis',
  'Xenova/bert-base-multilingual-uncased-sentiment'
);
```

**Finding Models:**

Browse available Transformers.js models on Hugging Face Hub:
- **All models**: https://huggingface.co/models?library=transformers.js&sort=trending
- **By task**: Add `pipeline_tag` parameter
  - Text generation: https://huggingface.co/models?pipeline_tag=text-generation&library=transformers.js&sort=trending
  - Image classification: https://huggingface.co/models?pipeline_tag=image-classification&library=transformers.js&sort=trending
  - Speech recognition: https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&library=transformers.js&sort=trending

**Tip:** Filter by task type, sort by trending/downloads, and check model cards for performance metrics and usage examples.

### 3. Device Selection
Choose where to run the model:

```javascript
// Run on CPU (default for WASM)
const pipe = await pipeline('sentiment-analysis', 'model-id');

// Run on GPU (WebGPU)
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  device: 'webgpu',
});
```

### 4. Quantization Options
Control model precision vs. performance:

```javascript
// Use quantized model (faster, smaller)
const pipe = await pipeline('sentiment-analysis', 'model-id', {
  dtype: 'q4',  // Options: 'fp32', 'fp16', 'q8', 'q4'
});
```

## Supported Tasks

**Note:** All examples below show basic usage.

### Natural Language Processing

#### Text Classification
```javascript
const classifier = await pipeline('text-classification');
const result = await classifier('This movie was amazing!');
```

#### Named Entity Recognition (NER)
```javascript
const ner = await pipeline('token-classification');
const entities = await ner('My name is John and I live in New York.');
```

#### Question Answering
```javascript
const qa = await pipeline('question-answering');
const answer = await qa({
  question: 'What is the capital of France?',
  context: 'Paris is the capital and largest city of France.'
});
```

#### Text Generation
```javascript
const generator = await pipeline('text-generation', 'onnx-community/gemma-3-270m-it-ONNX');
const text = await generator('Once upon a time', {
  max_new_tokens: 100,
  temprature: 0.7
}