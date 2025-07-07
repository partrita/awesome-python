#!/usr/bin/env python
# coding: utf-8

"""
    취해진 접근 방식은 아래에 설명되어 있습니다. 간단하게 하기로 결정했습니다.
    처음에는 데이터를 어떤 종류의 구조로 구문 분석한 다음 적절한 README를 생성하는 것을 고려했습니다.
    여전히 고려 중이지만 지금은 이것으로 충분할 것입니다. 유일한 문제는 가장 낮은 수준의 항목만 정렬하고
    최상위 콘텐츠의 순서가 실제 항목의 순서와 일치하지 않는다는 것입니다.

    이것은 중첩된 블록을 갖고 재귀적으로 정렬한 다음 최종 구조를 줄 목록으로 평면화하여 확장할 수 있습니다.
    아마도 개정 2에서요 ^.^.
"""

def sort_blocks():
    # 먼저 현재 README를 메모리로 로드합니다.
    with open('README.md', 'r') as read_me_file:
        read_me = read_me_file.read()

    # '목차'를 내용(블록)과 분리합니다.
    table_of_contents = ''.join(read_me.split('- - -')[0])
    blocks = ''.join(read_me.split('- - -')[1]).split('\n# ')
    for i in range(len(blocks)):
        if i == 0:
            blocks[i] = blocks[i] + '\n'
        else:
            blocks[i] = '# ' + blocks[i] + '\n'

    # 라이브러리 정렬
    inner_blocks = sorted(blocks[0].split('##'))
    for i in range(1, len(inner_blocks)):
        if inner_blocks[i][0] != '#':
            inner_blocks[i] = '##' + inner_blocks[i]
    inner_blocks = ''.join(inner_blocks)

    # 정렬되지 않은 라이브러리를 정렬된 라이브러리로 바꾸고 final_README 파일에 모두 모읍니다.
    blocks[0] = inner_blocks
    final_README = table_of_contents + '- - -' + ''.join(blocks)

    with open('README.md', 'w+') as sorted_file:
        sorted_file.write(final_README)

def main():
    # 먼저 현재 README를 줄 배열로 메모리에 로드합니다.
    with open('README.md', 'r') as read_me_file:
        read_me = read_me_file.readlines()

    # 그런 다음 줄을 블록으로 함께 클러스터링합니다.
    # 각 블록은 정렬해야 하는 줄 모음을 나타냅니다.
    # 이것은 링크([...](...))만 정렬되도록 가정하여 수행되었습니다.
    # 클러스터링은 들여쓰기로 수행됩니다.
    blocks = []
    last_indent = None
    for line in read_me:
        s_line = line.lstrip()
        indent = len(line) - len(s_line)

        if any([s_line.startswith(s) for s in ['* [', '- [']]):
            if indent == last_indent:
                blocks[-1].append(line)
            else:
                blocks.append([line])
            last_indent = indent
        else:
            blocks.append([line])
            last_indent = None

    with open('README.md', 'w+') as sorted_file:
        # 그런 다음 모든 블록을 개별적으로 정렬합니다.
        blocks = [
            ''.join(sorted(block, key=str.lower)) for block in blocks
        ]
        # 그리고 결과를 README.md에 다시 씁니다.
        sorted_file.write(''.join(blocks))

    # 그런 다음 정렬 방법을 호출합니다.
    sort_blocks()


if __name__ == "__main__":
    main()
