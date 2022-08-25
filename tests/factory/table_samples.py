table_with_header = """
<table>
    <tr>
        <th>Height</th><th>Width</th><th>Depth</th>
    </tr>
    <tr>
        <td>10</td><td>12</td><td>5</td>
    </tr>
    <tr>
        <td>2</td><td>3</td><td>5</td>
    </tr>
</table>
"""

table_without_header = """
<div>
    <p>This text should be ignored by TableReader.</p>
</div>
<table>
    <tr>
        <td>Height</td><td>2</td>
    </tr>
    <tr>
        <td>Width</td><td>3</td>
    </tr>
</table>
<div>
    <p>This text should be ignored by TableReader.</p>
</div>
"""

table_without_header_v2 = """
<table>
    <tr>
        <td>DIMENSIONS:</td><td></td><td></td>
    </tr>
    <tr>
        <td>Height</td><td>2</td><td>4</td>
    </tr>
    <tr>
        <td>Width</td><td>3</td><td>8</td>
    </tr>
</table>
"""

table_without_header_v3 = """
<table>
    <tbody>
        <tr>
            <td scope="row">Type</td>
            <td>Easybook Pro</td>
        </tr>
        <tr>
            <td scope="row">Operating system</td>
            <td>etOS</td>
        </tr>
    </tbody>
</table>
"""

table_without_header_v4 = """
<table>
    <tr>
        <th scope="row">Type</th>
        <td>Easybook Pro</td>
    </tr>
    <tr>
        <th scope="row">Operating system</th>
        <td>etOS</td>
    </tr>
</table>
"""
