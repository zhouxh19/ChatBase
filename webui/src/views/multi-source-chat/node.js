
export function generateNode(id, data) {
  return {
    id,
    position: { x: 0, y: 0 },
    type: 'process',
    data
  }
}
