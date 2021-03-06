import argparse


class StoreDictKeyPairs(argparse.Action):

    """
    custom action to create a dict from a provided string in the format of key=value
    """

    retval = {}

    def __call__(self, parser, namespace, values, option_string=None):
        for kv in values.split(","):
            if "=" in kv:
                splitter = "="
            else:
                splitter = ":"
            if kv.count(splitter) != 1:
                first_equal_index = kv.index(splitter)
                key = kv[:first_equal_index].strip()
                value = kv[first_equal_index + 1:].strip()
                self.retval[key] = value
            else:
                k, v = kv.split(splitter)
                self.retval[k.strip()] = v.strip()
        setattr(namespace, self.dest, self.retval)


class BucketDumpParser(argparse.ArgumentParser):

    def __init__(self):
        super(BucketDumpParser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        parser.add_argument("-q", "--query", metavar="SEARCH-QUERY", dest="searchQuery",
                            help="provide a search query to search open buckets with")
        parser.add_argument("-b", "--bucket", metavar="BUCKET-URL", dest="getThisBucket",
                            help="Specify a single bucket URL and download all open and available files from "
                                 "the single bucket"),
        parser.add_argument('-l', "--list", metavar="FILE-PATH", dest="searchQueries",
                            help="Provide a textual file of search queries, one per line"),
        parser.add_argument("--random-agent", action="store_true", dest="randomAgent",
                            help="Use a random HTTP User-Agent")
        parser.add_argument("--verbose", action="store_true", dest="runVerbose",
                            help="Run in verbose mode")
        parser.add_argument("-P", "--proxy", metavar="PROXY", dest="useProxy",
                            help="Use a proxy for the requests")
        parser.add_argument("-H", "--headers", metavar="HEADER=1,HEADER:2,etc..", dest="extraHeaders",
                            action=StoreDictKeyPairs, help="Pass extra headers with your request")
        parser.add_argument("-s", "--search", metavar="STRING", dest="fileSearch",
                            help="Search for a file and output the location of it")
        parser.add_argument("--check-proxy", action="store_true", dest="verifyProxy",
                            help="Verify that your proxy is working correctly")
        parser.add_argument("--swim", action="store_true", dest="spiderFoundBucket",
                            help="Swim upstream to the found bucket and try to pull everything out of it")
        parser.add_argument("--limit", type=int, default=300, metavar="AMOUNT", dest="bucketsToPull",
                            help="Used in conjunction with `--swim` specify an amount of buckets to pull "
                                 "(*default=300)")
        parser.add_argument("--download-anyways", action="store_true", default=False, dest="downloadAnyways",
                            help=argparse.SUPPRESS)
        return parser.parse_args()