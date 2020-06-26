import json
from snflambda import snf
from smithnormalform import matrix, snfproblem, z, zi


event_mock_filename = 'data/lambda-event-mock.json'


def test_too_large_magnitude():
    requestBody = {
                    "type": "problem",
                    "ring": "z",
                    "height": 1,
                    "width": 1,
                    "contents": [1e6]
                  }

    with open(event_mock_filename, 'r') as f:
        f_contents = f.read()

    eventObj = json.loads(f_contents)
    eventObj['body'] = json.dumps(requestBody)
    eventObj['isBase64Encoded'] = False

    result = snf.snf_handler(eventObj, None)

    assert(result['status'] == 403)


def test_too_large_dimension():
    requestBody = {
                    "type": "problem",
                    "ring": "z",
                    "height": 11,
                    "width": 1,
                    "contents": [1]*11
                  }

    with open(event_mock_filename, 'r') as f:
        f_contents = f.read()

    eventObj = json.loads(f_contents)
    eventObj['body'] = json.dumps(requestBody)
    eventObj['isBase64Encoded'] = False

    result = snf.snf_handler(eventObj, None)

    assert(result['status'] == 403)


def test_bad_ring():
    requestBody = {
                    "type": "problem",
                    "ring": "unsupported ring",
                    "height": 1,
                    "width": 1,
                    "contents": [1]
                  }

    with open(event_mock_filename, 'r') as f:
        f_contents = f.read()

    eventObj = json.loads(f_contents)
    eventObj['body'] = json.dumps(requestBody)
    eventObj['isBase64Encoded'] = False

    result = snf.snf_handler(eventObj, None)

    assert(result['status'] == 400)


def test_bad_operation():
    requestBody = {
                    "type": "unsupported operation",
                    "ring": "z",
                    "height": 1,
                    "width": 1,
                    "contents": [1]
                  }

    with open(event_mock_filename, 'r') as f:
        f_contents = f.read()

    eventObj = json.loads(f_contents)
    eventObj['body'] = json.dumps(requestBody)
    eventObj['isBase64Encoded'] = False

    result = snf.snf_handler(eventObj, None)

    assert(result['status'] == 400)
