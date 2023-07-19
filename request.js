const fetch = require('node-fetch');

async function extractTexts() {
  const fs = require('fs');
  const imageBuffer = fs.readFileSync('cropped_image.png');
  const encodedImage = imageBuffer.toString('base64');

  const body = {
    folderId: 'b1g3ki01pbguna3cb7q1',
    analyze_specs: [{
      content: encodedImage,
      features: [{
        type: 'TEXT_DETECTION',
        text_detection_config: {
          language_codes: ['*']
        }
      }]
    }]
  };

  const headers = {
    'Content-Type': 'application/json',
    Authorization: 'Bearer t1.9euelZqdx4nKzJSdzMaYi8uMksvMiu3rnpWayszJlZKVz5KJyceXmMyJyZvl9PckbWta-e86WjTg3fT3ZBtpWvnvOlo04M3n9euelZrJy52Pm5uLiZSbxs3Ij5zPlu_8xeuelZrJy52Pm5uLiZSbxs3Ij5zPlg.wgrqke5bJx7KpOX-aJXM3iPvSAuRyNOWNlMax3xFmtwpkyGYiuVkKo3_NgwTmXNq9J15LTOyWf8uhacxsViYCw'
  };

  const response = await fetch('https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze', {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(body)
  });

  const json_data = await response.json();
  const texts = [];

  const results = json_data.results;
  for (const result of results) {
    const resultsList = result.results;
    for (const res of resultsList) {
      const textDetection = res.textDetection;
      const pages = textDetection.pages;
      for (const page of pages) {
        const blocks = page.blocks;
        for (const block of blocks) {
          const lines = block.lines;
          for (const line of lines) {
            const words = line.words;
            for (const word of words) {
              const text = word.text;
              texts.push(text);
            }
          }
        }
      }
    }
  }

  return texts;
}

extractTexts()
  .then(texts => {
    console.log(texts);
  })
  .catch(error => {
    console.error(error);
  });
