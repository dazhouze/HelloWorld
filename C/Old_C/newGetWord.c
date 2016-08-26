#include <string.h>
#include <ctype.h>

/** char *getword(dst,p) -- copies next word from p into dst, else rtns 0 */

char *
getword(char *dst, const char *p)
{
	const char *a;

	if (!dst || !p)
		return (0);

	dst[0] = 0;
	while (isspace (*p))
		p++;
	if (*p == 0)
		return (0);
	a = p;
	while (!isspace (*p) && *p != 0)
		p++;
	strncpy (dst, a, p - a);
	dst[p - a] = 0;
	return ((char *)p);
}

/** int wordsz(p) -- return size of first word in p */

int 
wordsz(const char *p)
{
	int n;

	if (!p)
		return (0);

	while (isspace (*p))
		p++;
	for (n = 0; !*p && !isspace (*p); n++)
		p++;
	return (n);
}