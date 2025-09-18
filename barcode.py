import cv2
from pyzbar.pyzbar import decode


def scan_barcode_from_image(image_path):
    """
    Scans and prints barcode data from the given image file.
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not read image: {image_path}")
        return
    barcodes = decode(img)
    if not barcodes:
        print("No barcode found.")
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        print(f"Found {barcode_type} barcode: {barcode_data}")


def scan_barcode_from_webcam():
    """
    Scans barcodes using the webcam and prints their data.
    Press 'q' to quit.
    """
    cap = cv2.VideoCapture(0)
    print("Starting webcam. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            print(f"Found {barcode_type} barcode: {barcode_data}")
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow('Barcode Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        scan_barcode_from_image(sys.argv[1])
    else:
        scan_barcode_from_webcam()
