export function getTextWidth(text: string, font: string): number | undefined {
  var canvas = document.createElement('canvas');
  var context = canvas.getContext('2d');
  if (context) {
    context.font = font;
    var metrics = context.measureText(text);
    return metrics.width;
  }
}
