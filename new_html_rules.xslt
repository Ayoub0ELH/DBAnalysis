<!-- games.xslt -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <head>
        <title>Game Data</title>
      </head>
      <body>
        <h1>Game Data</h1>
        <table border="1">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Platform</th>
            <th>Year</th>
            <th>Genre</th>
            <th>Publisher</th>
            <th>Sales North America</th>
            <th>Sales Europe</th>
            <th>Sales Japan</th>
            <th>Sales Other</th>
            <th>Sales Global</th>
          </tr>
          <xsl:for-each select="games/game">
            <tr>
              <td><xsl:value-of select="ID"/></td>
              <td><xsl:value-of select="Name"/></td>
              <td><xsl:value-of select="Platform"/></td>
              <td><xsl:value-of select="Year"/></td>
              <td><xsl:value-of select="Genre"/></td>
              <td><xsl:value-of select="Publisher"/></td>
              <td><xsl:value-of select="Sales/@North_America"/></td>
              <td><xsl:value-of select="Sales/@Europe"/></td>
              <td><xsl:value-of select="Sales/@Japan"/></td>
              <td><xsl:value-of select="Sales/@Other"/></td>
              <td><xsl:value-of select="Sales/@Global"/></td>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>