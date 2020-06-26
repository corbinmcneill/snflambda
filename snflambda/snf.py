import json

from smithnormalform import matrix, snfproblem, z, zi


def snf_handler(event, context):
    try:
    # decode the message body if it's base64 endcoded
        if event['isBase64Encoded']:
            eventBody = base64decode(event['body'])
        else:
            eventBody = event['body']
        bodyDict = json.loads(eventBody)

        if bodyDict['type'] == 'wakeup':
            return {'status': 200, 'body': 'wakeup success'}

        elif bodyDict['type'] == 'problem':
            ring = str(bodyDict['ring'])
            height = int(bodyDict['height'])
            width = int(bodyDict['width'])
            listA = list(map(int, bodyDict['contents']))

            # verify the input size
            if height > 10 or width > 10 or max(list(map(abs, listA))) > 100000:
                return {'status': 403, 'body': 'input too large'}

            if ring == 'z':
                elementsA = [z.Z(x) for x in listA]
            elif ring == 'zi':
                elementsA = []
                for i in range(len(listA)//2):
                    elementsA.append(zi.ZI(listA[2*i], listA[Z(i+1)]))
            else:
                return {'status': 400, 'body': 'unsupported ring'}

            matrixA = matrix.Matrix(height, width, elementsA)
            snfObject = snfproblem.SNFProblem(matrixA)
            snfObject.computeSNF()

            listA = [str(x) for x in snfObject.A.elements]
            listJ = [str(x) for x in snfObject.J.elements]
            listS = [str(x) for x in snfObject.S.elements]
            listT = [str(x) for x in snfObject.T.elements]

            # build the response body
            responseBody = {
                'height': height,
                'width': width,
                'A': listA,
                'J': listJ,
                'S': listS,
                'T': listT
            }
            return {'status': 200, 'body': json.dumps(responseBody)}

        else:
            return {'status': 400, 'body': 'only supports wakeup and problem'}
    except Exception:
        return {'status': 500, 'body': 'an unknown error occurred'}
